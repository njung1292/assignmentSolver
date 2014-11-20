from collections import Counter
from munkres import Munkres
from dataGen import DataGen
from data import Data
from makeExcel import makeExcel
import logging
import argparse
import time

def solve(data):
    """Applies the Hungarian algorithm to the data."""

    start = time.clock() # Start timing computation time
    rankMatrix = data.makeMatrix()
    m = Munkres()
    logging.info("Running the Hungarian algorithm...")
    indexes = m.compute(rankMatrix)
    end     = time.clock() # Stop timer
    
    solution = []
    total = 0
    i = 0
    for row, column in indexes:
        value = rankMatrix[row][column]
        solution.append([data.names[row], data.columnToSeminar(column), value])
        total += value
        logging.debug(' (%d) %s -> %s', value, solution[i][0], solution[i][1])
        i += 1 
    print '> Total cost  : %d' % total
    print '> Time elapsed: %f' % (end - start)
    # makeExcel(solution)
    return solution

def test():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',
        help='Print lots of debugging statements',
        action="store_const",dest="loglevel",const=logging.DEBUG,
        default=logging.WARNING
    )
    parser.add_argument('-v','--verbose',
        help='Be verbose',
        action="store_const",dest="loglevel",const=logging.INFO
    )
    args = parser.parse_args()    
    logging.basicConfig(format='%(levelname)s:  %(message)s',level=args.loglevel)

    # numStudents = 350
    # fallList    = ['f01','f02','f03','f04','f05','f06','f07','f08','f09','f10','f11']
    # springList  = ['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11']

    # numStudents = 100
    # fallList    = ['f01','f02','f03','f04','f05']
    # springList  = ['s01','s02','s03','s04','s05']

    # dg       = DataGen(fallList, springList, numStudents)
    # names    = dg.generateNames()
    # topFives = dg.generateRanks()

    numStudents = 5
    fallList    = ['f01', 'f02']
    springList  = ['s01', 's02']
    names       = ['A', 'B', 'C', 'D', 'E']
    topFives    = [['s01', 'f01', 's02'],
                   ['s02', 'f02', 'f01'],
                   ['f02', 's02', 's01'],
                   ['s01', 'f02', 's02'],
                   ['f01', 's01', 's02']]

    data     = Data(names, topFives, fallList, springList)
    solution = solve(data)

    seminarCounts = Counter()
    for decision in solution:
        seminarCounts[decision[1]] += 1

    print "> Seminar Counts: "
    print "> " + str(seminarCounts)

if __name__ == '__main__':
    test()
