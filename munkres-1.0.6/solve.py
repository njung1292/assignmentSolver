from collections import Counter
from munkres import Munkres
from dataGen import DataGen
from data import Data
import time

def solve(data):
    """Applies the Hungarian algorithm to the data."""

    start = time.clock() # Start timing computation time
    rankMatrix = data.makeMatrix()
    m = Munkres()
    
    print "Running the Hungarian algorithm..."
    indexes = m.compute(rankMatrix)
    end     = time.clock() # Stop timer
    
    solution = []
    total = 0
    for row, column in indexes:
        solution.append([data.names[row], data.indexToSeminar(column)])
        value = rankMatrix[row][column]
        total += value
        # print ' (%d) %s -> %s' % (value, data.names[row], data.indexToSeminar(column)) 
    print 'Total cost: %d' % total
    print 'Time elapsed: %f' % (end - start)
    return solution

def test():
    numStudents = 350
    fallList    = ['f01','f02','f03','f04','f05','f06','f07','f08','f09','f10','f11']
    springList  = ['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11']
    # numStudents = 100
    # fallList    = ['f01','f02','f03','f04','f05']
    # springList  = ['s01','s02','s03','s04','s05']
    dg       = DataGen(fallList, springList, numStudents)
    names    = dg.generateNames()
    topFives = dg.generateRanks()
    data     = Data(names, topFives, fallList, springList)
    solution = solve(data)

    seminarCounts = Counter()
    for decision in solution:
        # print decision
        seminarCounts[decision[1]] += 1
    print seminarCounts

test()