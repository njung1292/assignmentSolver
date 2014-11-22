import random
import logging

class DataGen:
    """Class that randomly generates data."""

    def __init__(self, fallList, springList, numStudents):
        """Create a new instance."""

        self.fallList    = fallList
        self.springList  = springList
        self.numStudents = numStudents

    def generateNames(self):
        """Returns a list of unique strings representing student names."""

        logging.info("Generating names...")

        k = 0
        names = []
        for i in range(97,123):
            for j in range(97,111):
                names.append(str(unichr(i))+str(unichr(j)))
                k += 1
                if (k == self.numStudents):
                    return names

    def generateRanks(self):
        """Returns a 2D list of top 5 seminars for each student."""
        logging.info("Generating rankings...")

        bigList   = []
        numFall   = len(self.fallList)
        numSpring = len(self.springList)
        for student in range(0, self.numStudents):
            myList = []

            # fall semester
            a = random.randint(0, numFall - 1)
            b = random.randint(0, numFall - 1)
            while (a == b):
                b = random.randint(0, numFall - 1)
            myList.append(self.fallList[a])
            myList.append(self.fallList[b])

            # spring semester
            c = random.randint(numFall, numFall + numSpring - 1)
            d = random.randint(numFall, numFall + numSpring - 1)
            while (c == d):
                d = random.randint(numFall, numFall + numSpring - 1)
            myList.append(self.springList[c - numFall])
            myList.append(self.springList[d - numFall])

            # last seminar
            e = random.randint(0, numFall + numSpring - 1)
            while (e == a or e == b or e == c or e == d):
                e = random.randint(0, numFall + numSpring - 1)
            if (e < numFall):
                myList.append(self.fallList[e])
            else:
                myList.append(self.springList[e - numFall])

            random.shuffle(myList)
            bigList.append(myList)

        return bigList


# def seminarPopularity(bigList, fallList, springList):
#     yearList = fallList + springList
#     initial = []
#     for i in range(len(yearList)):
#         initial.append((yearList[i], 0))
#     seminarDict = dict(initial)
#     for i in range(len(bigList)):
#         for j in range(len(bigList[0])):
#             seminarDict[bigList[i][j]] += 1
#     sorted_seminar = sorted(seminarDict.items(), key=operator.itemgetter(1), reverse = True)
#     finalList = []
#     for i in range(len(sorted_seminar)):
#         finalList.append(sorted_seminar[i][0])
#     return finalList
            

# totalStudents = 350 
# fallList = []
# springList = []
# for i in xrange(1,13):
#     fallList.append("f" + str(i))
#     springList.append("s" + str(i))


# bigList = dataGenerator(fallList, springList, totalStudents)
# seminarPopularity(bigList, fallList, springList)
        
    
