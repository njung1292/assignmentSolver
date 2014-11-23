from collections import Counter
import logging, operator, random

MIN_ORD = 97

class Data:
    """ Class that contains data (e.g. names, number of students, seminar lists)"""

    def __init__(self, rank_matrix, year_list):
        """Create a new instance"""
        # Set data fields
        self.names            = range(1, len(rank_matrix)+1)
        self.year_list        = year_list
        self.rank_matrix      = []
        self.num_students     = len(rank_matrix)
        self.num_seminars     = len(year_list)
        self.popular_seminars = [] # Most popular seminars (int index, int count)

        # Rank the seminars by popularity
        seminar_ctr = Counter()
        for i in range(self.num_students):
            for j in range(self.num_seminars):
                if (rank_matrix[i][j] < 100):
                    seminar_ctr[j] += 1
        self.popular_seminars = seminar_ctr.most_common()
        logging.debug("Popular seminars: " + str(self.popular_seminars))

        # Extend the rank matrix
        num_extra = self.num_students % self.num_seminars
        seminar_size = self.num_students / self.num_seminars
        for row in rank_matrix:
            row *= seminar_size
            for popular_seminar in self.popular_seminars[0:num_extra]:
                row.append(row[popular_seminar[0]])
            self.rank_matrix.append(row)

    def col_to_sem(self, col):
        """Converts a rank matrix column to the seminar name."""
        seminar_size = self.num_students / self.num_seminars
        c = col % self.num_seminars
        if ((col / self.num_seminars) >= seminar_size):
            return self.year_list[self.popular_seminars[c][0]]
        else:
            return self.year_list[c]

    @staticmethod
    def factory(num_students, num_seminars):
        """ Returns a randomly generated instance of Data_b given the number of
            students and seminars """
        fall_list = []
        spring_list = []

        # Generate a list of fall and spring classes
        for i in range(num_seminars/2):
            fall_list.append("F" + '%02d'%(i+1))
            spring_list.append("S" + '%02d'%(i+1))
        if (num_seminars % 2 == 1):
            fall_list.append("F" + str(num_seminars/2 + 1))    

        # Generate a list of names
        assert num_students < 26*26
        names = ['']*num_students
        for i in range(num_students):
            name = str(chr(MIN_ORD + i/26)) + str(chr(MIN_ORD + i))
            names[i] = name

        # Generate a matrix of seminar rankings for each student
        num_fall     = len(fall_list)
        num_spring   = len(spring_list)
        rank_matrix  = [[]]*num_students
        seminar_size = num_students / num_seminars
        num_extra = num_students % num_seminars
        for i in range(num_students):
            row = [100]*num_seminars
            top_five = [-1]*5

            # fall semester
            assert num_fall > 3
            f1, f2, r1 = random.sample(range(num_fall), 3)
            top_five[0] = f1
            top_five[1] = f2

            # spring semester
            assert num_spring > 2
            s1, s2 = random.sample(range(num_fall, num_fall + num_spring), 2)
            top_five[2] = s1
            top_five[3] = s2

            # last seminar
            last_sem = r1 if (r1%2 == 0) else (r1 + num_fall - 1)
            assert last_sem < num_seminars
            top_five[4] = last_sem
            
            random.shuffle(top_five)

            for j in range(5): # We are guaranteed to need to check 5
                row[top_five[j]] = j+1
            rank_matrix[i] = row

        return Data(rank_matrix, fall_list + spring_list)
