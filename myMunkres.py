#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
Modified from the python munkres module written by Brian Clapper.

Copyright and License
=====================

This software is released under a BSD license, adapted from
<http://opensource.org/licenses/bsd-license.php>

Copyright (c) 2008 Brian M. Clapper
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name "clapper.org" nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

__docformat__ = 'restructuredtext'

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import copy

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__     = ['Munkres', 'make_cost_matrix']

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

# Info about the module
__version__   = "1.0.6"
__author__    = "Brian Clapper, bmc@clapper.org"
__url__       = "http://software.clapper.org/munkres/"
__copyright__ = "(c) 2008 Brian M. Clapper"
__license__   = "BSD-style license"

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class Munkres:
    """
    Calculate the Munkres solution to the classical assignment problem.
    See the module documentation for usage.
    """

    def __init__(self):
        """Create a new instance"""
        self.C = None
        self.row_covered = []
        self.col_covered = []
        self.n = 0
        self.Z0_r = 0
        self.Z0_c = 0
        self.marked = None # Cell values: 1:=starred, 2:=primed, 0:=none
        self.path = None

    def make_cost_matrix(profit_matrix, inversion_function):
        """
        **DEPRECATED**

        Please use the module function ``make_cost_matrix()``.
        """
        import munkres
        return munkres.make_cost_matrix(profit_matrix, inversion_function)

    make_cost_matrix = staticmethod(make_cost_matrix)

    # def pad_matrix(self, matrix, pad_value=0):
    #     """
    #     Pad a possibly non-square matrix to make it square.

    #     :Parameters:
    #         matrix : list of lists
    #             matrix to pad

    #         pad_value : int
    #             value to use to pad the matrix

    #     :rtype: list of lists
    #     :return: a new, possibly padded, matrix
    #     """
    #     max_columns = 0
    #     total_rows = len(matrix)

    #     for row in matrix:
    #         max_columns = max(max_columns, len(row))

    #     total_rows = max(max_columns, total_rows)

    #     new_matrix = []
    #     for row in matrix:
    #         row_len = len(row)
    #         new_row = row[:]
    #         if total_rows > row_len:
    #             # Row too short. Pad it.
    #             new_row += [0] * (total_rows - row_len)
    #         new_matrix += [new_row]

    #     while len(new_matrix) < total_rows:
    #         new_matrix += [[0] * total_rows]

    #     return new_matrix

    def compute(self, cost_matrix):
        """
        Compute the indexes for the lowest-cost pairings between rows and
        columns in the database. Returns a list of (row, column) tuples
        that can be used to traverse the matrix.

        :Parameters:
            cost_matrix : list of lists
                The cost matrix. If this cost matrix is not square, it
                will be padded with zeros, via a call to ``pad_matrix()``.
                (This method does *not* modify the caller's matrix. It
                operates on a copy of the matrix.)

                **WARNING**: This code handles square and rectangular
                matrices. It does *not* handle irregular matrices.

        :rtype: list
        :return: A list of ``(row, column)`` tuples that describe the lowest
                 cost path through the matrix

        """
        # self.C = self.pad_matrix(cost_matrix)
        self.C = self.__copy_matrix(cost_matrix)
        self.n = len(self.C)
        self.original_length = len(cost_matrix)
        self.original_width = len(cost_matrix[0])
        self.row_covered = [False for i in xrange(0, self.n)]
        self.col_covered = [False for i in xrange(0, self.n)]
        self.Z0_r = 0
        self.Z0_c = 0
        self.path = self.__make_matrix(self.n * 2, 0)
        self.marked = self.__make_matrix(self.n, 0)
        self.primes = []

        done = False
        step = 1

        steps = { 1 : self.__step1,
                  2 : self.__step2,
                  3 : self.__step3,
                  4 : self.__step4,
                  5 : self.__step5,
                  6 : self.__step6 }

        while not done:
            try:
                func = steps[step]
                step = func()
            except KeyError:
                done = True

        print "Done!"
        print ""

        # Look for the starred columns
        results = []
        for i in xrange(0, self.original_length):
            for j in xrange(0, self.original_width):
                if self.marked[i][j] == 1:
                    results += [(i, j)]

        return results

    def __printCovering(self):
        coverMatrix = []
        for i in self.row_covered:
            row = []
            for j in self.col_covered:
                if (i or j):
                    row.append(1)
                else:
                    row.append(0)
            coverMatrix.append(row)
        print ""
        print_matrix(coverMatrix, "Current covering:")

    def __copy_matrix(self, matrix):
        """Return an exact copy of the supplied matrix"""
        return copy.deepcopy(matrix)

    def __make_matrix(self, n, val):
        """Create an *n*x*n* matrix, populating it with the specific value."""
        matrix = []
        for i in xrange(0, n):
            matrix += [[val for j in xrange(0, n)]]
        return matrix

    def __step1(self):
        """
        For each row of the matrix, find the smallest element and
        subtract it from every element in its row. Go to Step 2.
        """

        print ""
        print "Step 1: Row reduction"
        C = self.C
        n = self.n
        for i in xrange(0, n):
            # minval = min(self.C[i])
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
            ## !!!THE MINVAL IN THIS STEP WILL ALWAYS BE 1 FOR OUR PURPOSES !!!
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
            minval = 1
            # Find the minimum value for this row and subtract that minimum
            # from every element in the row.
            for j in xrange(0, n):
                self.C[i][j] -= minval

        print_matrix(self.C)
        return 2

    def __step2(self):
        """
        Find a zero (Z) in the resulting matrix. If there is no starred
        zero in its row or column, star Z. Repeat for each element in the
        matrix. Go to Step 3.
        """

        print ""
        print "Step 2: Finding an initial matching..."
        n = self.n
        count = 0
        covered_rows = [] # keep track of covered rows so you can clear them
        for i in xrange(0, n):
            if (not self.row_covered[i]): # CHECK THE ROW HERE!
                for j in xrange(0, n):
                    if (self.C[i][j] == 0) and \
                            (not self.col_covered[j]) and \
                            (not self.row_covered[i]):
                        self.marked[i][j] = 1
                        self.col_covered[j] = True
                        self.row_covered[i] = True
                        covered_rows.append(i)
                        count += 1
                        break # found a zero to star, so you can go to the next row (i think??)

        print_matrix(self.marked)

        # self.__clear_covers() # why?? May just need to clear the rows:
        for i in covered_rows:
            self.row_covered[i] = False

        self.__printCovering()

        # return 3
        if count >= n:
            step = 7 # done
        else:
            step = 4

        return step


    def __step3(self):
        """
        Cover each column containing a starred zero. If n columns are
        covered, the starred zeros describe a complete set of unique
        assignments. In this case, Go to DONE, otherwise, Go to Step 4.
        """

        print ""
        print "Step 3"
        n = self.n
        count = 0
        for i in xrange(0, n):
            for j in xrange(0, n):
                if self.marked[i][j] == 1:
                    self.col_covered[j] = True
                    count += 1

        if count >= n:
            step = 7 # done
        else:
            step = 4

        return step

    def __step4(self):
        """
        Find a noncovered zero and prime it. If there is no starred zero
        in the row containing this primed zero, Go to Step 5. Otherwise,
        cover this row and uncover the column containing the starred
        zero. Continue in this manner until there are no uncovered zeros
        left.
        """

        print ""
        print "Step 4: ",
        step = 0
        done = False
        row = -1
        col = -1
        star_col = -1
        while not done:
            print "Finding a noncovered zero to prime.."
            (row, col) = self.__find_a_zero()
            if row < 0:
                done = True
                step = 6
            else:
                # Found a noncovered zero
                self.marked[row][col] = 2 # Prime the noncovered zero
                self.primes.append([row,col]) # Add to the list of primes
                print "--> Primed (%d, %d)" % (row,col)
                print_matrix(self.marked)
                print ""
                print "--> Finding a star in row %d..." % row
                star_col = self.__find_star_in_row(row)
                if star_col >= 0:
                    print "--> Found star at (%d, %d)" % (row, star_col)
                    print "--> Updating covering..."
                    col = star_col
                    self.row_covered[row] = True
                    self.col_covered[col] = False
                    self.__printCovering()
                else:
                    print "--> No star"
                    # There is no starred zero in the row
                    done = True
                    # Save the location of the non/uncovered primed zero
                    self.Z0_r = row
                    self.Z0_c = col
                    step = 5

        return step

    def __step5(self):
        """
        Construct a series of alternating primed and starred zeros as
        follows. Let Z0 represent the uncovered primed zero found in Step 4.
        Let Z1 denote the starred zero in the column of Z0 (if any).
        Let Z2 denote the primed zero in the row of Z1 (there will always
        be one). Continue until the series terminates at a primed zero
        that has no starred zero in its column. Unstar each starred zero
        of the series, star each primed zero of the series, erase all
        primes and uncover every line in the matrix. Return to Step 3
        """

        print ""
        print "Step 5: Creating a path..."
        count = 0
        path = self.path
        path[count][0] = self.Z0_r
        path[count][1] = self.Z0_c
        print "--> Added (%d, %d) to path" % (self.Z0_r, self.Z0_c)
        done = False
        while not done:
            row = self.__find_star_in_col(path[count][1])
            if row >= 0:
                count += 1
                print "--> Added (%d, %d) to path" % (row, path[count-1][1])
                path[count][0] = row
                path[count][1] = path[count-1][1]
            else:
                print "-->Done constructing path"
                done = True

            if not done:
                col = self.__find_prime_in_row(path[count][0])
                count += 1
                print "--> Added (%d, %d) to path" % (path[count-1][0], col)
                path[count][0] = path[count-1][0]
                path[count][1] = col

        self.__convert_path(path, count)
        self.__clear_covers()
        self.__erase_primes()
        return 3

    ### this is more like step 4a
    def __step6(self):
        """
        Find the smallest uncovered value in the matrix.
        Add it to every element of each covered
        row, and subtract it from every element of each noncovered column.
        Return to Step 4 without altering any stars, primes, or covered
        lines.
        """

        print ""
        print "Step 6: Subtract/Add min noncovered val"
        minval = self.__find_smallest()
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):     
                if self.row_covered[i]:
                    self.C[i][j] += minval
                if not self.col_covered[j]:
                    self.C[i][j] -= minval

        print_matrix(self.C, "New cost matrix:")
        return 4

    def __find_smallest(self):
        """Find the smallest uncovered value in the matrix."""
        minval = sys.maxsize
        for i in xrange(0, self.n):
            if (not self.row_covered[i]): # check if the row is covered here
                for j in xrange(0, self.n):
                    # if (not self.row_covered[i]) and (not self.col_covered[j]):
                    if (not self.col_covered[j]):
                        if minval > self.C[i][j]:
                            minval = self.C[i][j]
        return minval

    def __find_a_zero(self):
        """Find the first uncovered element with value 0"""
        row = -1
        col = -1
        i = 0
        n = self.n
        done = False

        while not done:
            j = 0
            while True:
                if (self.C[i][j] == 0) and \
                        (not self.row_covered[i]) and \
                        (not self.col_covered[j]):
                    row = i
                    col = j
                    done = True
                    break
                else:
                    j += 1
                    if j >= n:
                        break
            i += 1
            if i >= n:
                done = True

        return (row, col)

    def __find_star_in_row(self, row):
        """
        Find the first starred element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in xrange(0, self.n):
            if self.marked[row][j] == 1:
                col = j
                break

        return col

    def __find_star_in_col(self, col):
        """
        Find the first starred element in the specified col. Returns
        the row index, or -1 if no starred element was found.
        """
        row = -1
        for i in xrange(0, self.n):
            if self.marked[i][col] == 1:
                row = i
                break

        return row

    def __find_prime_in_row(self, row):
        """
        Find the first prime element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = -1
        for j in xrange(0, self.n):
            if self.marked[row][j] == 2:
                col = j
                break

        return col

    def __convert_path(self, path, count):
        for i in xrange(0, count+1):
            if self.marked[path[i][0]][path[i][1]] == 1:
                self.marked[path[i][0]][path[i][1]] = 0
            else:
                self.marked[path[i][0]][path[i][1]] = 1

    def __clear_covers(self):
        """Clear all covered matrix cells"""
        for i in xrange(0, self.n):
            self.row_covered[i] = False
            self.col_covered[i] = False

    def __erase_primes(self):
        """Erase all prime markings"""
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                if self.marked[i][j] == 2:
                    self.marked[i][j] = 0

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def make_cost_matrix(profit_matrix, inversion_function):
    """
    Create a cost matrix from a profit matrix by calling
    'inversion_function' to invert each value. The inversion
    function must take one numeric argument (of any type) and return
    another numeric argument which is presumed to be the cost inverse
    of the original profit.

    This is a static method. Call it like this:

    .. python::

        cost_matrix = Munkres.make_cost_matrix(matrix, inversion_func)

    For example:

    .. python::

        cost_matrix = Munkres.make_cost_matrix(matrix, lambda x : sys.maxsize - x)

    :Parameters:
        profit_matrix : list of lists
            The matrix to convert from a profit to a cost matrix

        inversion_function : function
            The function to use to invert each entry in the profit matrix

    :rtype: list of lists
    :return: The converted matrix
    """
    cost_matrix = []
    for row in profit_matrix:
        cost_matrix.append([inversion_function(value) for value in row])
    return cost_matrix

def print_matrix(matrix, msg=None):
    """
    Convenience function: Displays the contents of a matrix of integers.

    :Parameters:
        matrix : list of lists
            Matrix to print

        msg : str
            Optional message to print before displaying the matrix
    """
    import math

    if msg is not None:
        print(msg)

    # Calculate the appropriate format width.
    width = 0
    for row in matrix:
        for val in row:
            width = max(width, int(math.log10(val+1)) + 1)

    # Make the format string
    format = '%%%dd' % width

    # Print the matrix
    for row in matrix:
        sep = '['
        for val in row:
            sys.stdout.write(sep + format % val)
            sep = ', '
        sys.stdout.write(']\n')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    matrices = [
        # Square
        ([[400, 150, 400],
          [400, 450, 600],
          [300, 225, 300]],
         850),  # expected cost

        # Rectangular variant
        ([[400, 150, 400, 1],
          [400, 450, 600, 2],
          [300, 225, 300, 3]],
         452),  # expected cost


        # Square
        ([[10, 10,  8],
          [9,  8,  1],
          [9,  7,  4]],
         18),

        # Rectangular variant
        ([[10, 10,  8, 11],
          [9,  8,  1, 1],
          [9,  7,  4, 10]],
         15)]

    m = Munkres()
    for cost_matrix, expected_total in matrices:
        print_matrix(cost_matrix, msg='cost matrix')
        indexes = m.compute(cost_matrix)
        total_cost = 0
        for r, c in indexes:
            x = cost_matrix[r][c]
            total_cost += x
            print('(%d, %d) -> %d' % (r, c, x))
        print('lowest cost=%d' % total_cost)
        assert expected_total == total_cost
