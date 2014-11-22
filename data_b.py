from collections import Counter
import logging
import operator

class Data_b:
    """ Class that contains data (e.g. names, number of students, seminar lists)"""

    def __init__(self, rank_matrix, year_list):
        """Create a new instance"""
        # Set data fields
        self.rank_matrix      = rank_matrix
        self.names            = range(1,len(rank_matrix)+1)
        self.num_students     = len(rank_matrix)
        self.num_seminars     = len(year_list)
        self.popular_seminars = []

        # Rank the seminars by popularity
        seminar_ctr = Counter()
        for i in range(self.num_students):
            for j in range(self.num_seminars):
                if (rank_matrix[i][j] < 100): seminar_ctr[year_list[j]] += 1
        self.popular_seminars = seminar_ctr.most_common()
        logging.debug("Popular seminars: " + str(self.popular_seminars))

    def columnToSeminar(self, col):
        """Converts a rank matrix column to the seminar name."""
        seminar_size = self.num_students / self.num_seminars
        c = col % self.num_seminars
        if ((col / self.num_seminars) >= seminar_size):
            return self.popular_seminars[c][0]
        else:
            return self.year_list[c]

    def __getRank(self, seminar, topSeminars):
        """Returns a students ranking of a given seminar"""
        try:
            return topSeminars.index(seminar) + 1
        except ValueError:
            return 100