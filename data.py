from collections import Counter
import operator

class Data:
    """ Class that contains data (e.g. names, number of students, seminar lists)"""

    def __init__(self, names, topFives, fallList, springList):
        """Create a new instance"""

        # Set data fields
        self.names           = names
        self.topFives        = topFives
        self.fallList        = fallList
        self.springList      = springList
        self.yearList        = fallList + springList
        self.numStudents     = len(topFives)
        self.numSeminars     = len(fallList) + len(springList)
        self.popularSeminars = []

        # Rank the seminars by popularity
        seminarDict = Counter()
        for i in xrange(0, self.numStudents):
            for j in xrange(0, len(self.topFives[0])):
                seminarDict[self.topFives[i][j]] += 1
        self.popularSeminars = seminarDict.most_common()
        print "> Popular seminars: "
        print "> " + str(self.popularSeminars)
        print ""

    def makeMatrix(self):
        """Convert top five rankings (n x m) into an (n x n) matrix."""

        print "> Converting rankings to matrix form...",

        rankMatrix = []
        seminarSize = self.numStudents / self.numSeminars
        for i in xrange(0, self.numStudents):
            row   = []
            count = 0
            for seminar in self.yearList:
                if (count < 5):
                    row.append(self.__getRank(seminar, self.topFives[i]))
                else:
                    numRemaining = self.numSeminars - i
                    row += [100]*numRemaining
            row *= seminarSize
            numExtra = self.numStudents % self.numSeminars
            for popularSeminar in self.popularSeminars[0:numExtra]:
                row.append(self.__getRank(popularSeminar[0], self.topFives[i]))
            rankMatrix.append(row)

        print "Done"
        return rankMatrix

    def columnToSeminar(self, col):
        """Converts a rank matrix column to the seminar name."""

        seminarSize = self.numStudents / self.numSeminars
        c = col % self.numSeminars
        if ((col / self.numSeminars) >= seminarSize):
            return self.popularSeminars[c][0]
        else:
            return self.yearList[c]

    def __getRank(self, seminar, topSeminars):
        """Returns a students ranking of a given seminar"""

        try:
            return topSeminars.index(seminar) + 1
        except ValueError:
            return 100