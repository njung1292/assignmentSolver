from collections import Counter
import logging
import operator

class Data:
    """ Class that contains data (e.g. names, number of students, seminar lists)"""

    def __init__(self, names, top_fives, fall_list, spring_list):
        """Create a new instance"""

        # Set data fields
        self.names            = names              # Names of students (strings)
        self.year_list        = fall_list + spring_list
        self.num_students     = len(top_fives)
        self.num_seminars     = len(self.year_list)
        self.rank_matrix      = []
        self.popular_seminars = [] # Most popular seminars (int index, int count)

        # Rank the seminars by popularity
        seminar_ctr = Counter()
        for i in range(self.num_students):
            for j in range(len(top_fives[i])):
                seminar_ctr[top_fives[i][j]] += 1
        self.popular_seminars = seminar_ctr.most_common()
        logging.debug("Popular seminars: " + str(self.popular_seminars))

        # Get the rank matrix
        self.rank_matrix = self.__make_matrix(top_fives)

    def __make_matrix(self, top_fives):
        """Convert top five rankings (n x m) into an (n x n) matrix."""
        logging.info("Converting rankings to matrix form...")

        rank_matrix = []
        seminarSize = self.num_students / self.num_seminars
        numExtra = self.num_students % self.num_seminars
        for i in range(self.num_students):
            row = [100]*self.num_seminars
            topSeminars = top_fives[i]
            for j in range(len(topSeminars)):
                row[topSeminars[j]] = j+1
            row *= seminarSize
            for popularSeminar in self.popular_seminars[0:numExtra]:
                row.append(self.__getRank(popularSeminar[0], topSeminars))
            rank_matrix.append(row)

        return rank_matrix

    def col_to_sem(self, col):
        """Converts a rank matrix column to the seminar name."""
        seminarSize = self.num_students / self.num_seminars
        c = col % self.num_seminars
        if ((col / self.num_seminars) >= seminarSize):
            return self.year_list[self.popular_seminars[c][0]]
        else:
            return self.year_list[c]

    def __getRank(self, seminar, topSeminars):
        """Returns a students ranking of a given seminar"""
        try:
            return topSeminars.index(seminar) + 1
        except ValueError:
            return 100