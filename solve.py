from collections import Counter
from munkres import Munkres
from dataGen import DataGen
from data import Data
from data_b import Data_b
import xlwt
import xlrd
import logging
import argparse
import time

def solve(data):
    """Applies the Hungarian algorithm to the data."""
    start = time.clock() # Start timing computation time
    rm = data.makeMatrix()
    m = Munkres()
    # rm = data.rank_matrix
    logger.info("\n  Running the Hungarian algorithm...")
    indexes = m.compute(rm)
    end     = time.clock() # Stop timer
    
    solution = []
    total = 0
    i = 0
    logger.debug("Solution:")
    for row, column in indexes:
        value = rm[row][column]
        solution.append([data.names[row], data.columnToSeminar(column), value])
        total += value
        logger.debug(' (%d) %s -> %s', value, solution[i][0], solution[i][1])
        i += 1 
    print '  --> Total cost    : %d' % total
    print '  --> Time elapsed  : %f' % (end - start)
    # makeExcel(solution)
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

    # numStudents = 5
    # fallList    = ['f01', 'f02']
    # springList  = ['s01', 's02']
    # names       = ['A', 'B', 'C', 'D', 'E']
    # topFives    = [['s01', 'f01', 's02'],
    #                ['s02', 'f02', 'f01'],
    #                ['f02', 's02', 's01'],
    #                ['s01', 'f02', 's02'],
    #                ['f01', 's01', 's02']]

    data     = Data(names, topFives, fallList, springList)
    solution = solve(data)
    return solution

    # seminarCounts = Counter()
    # for decision in solution:
    #     seminarCounts[decision[1]] += 1

    # print "  --> Seminar Counts: " + str(seminarCounts.items())

def main(filename):
    if (filename == "test"):
        solution = test()
    else:
        # Read XLS into Data object
        wb = xlrd.open_workbook(filename)
        ws = wb.sheet_by_index(0)
        ##### Get seminar list
        seminar_list = [str(seminar) for seminar in ws.row_values(1,start_colx=9,end_colx=None)]
        ##### Get number of students and seminars
        num_students = ws.nrows - 2
        num_seminars = len(seminar_list)
        ##### Get ranking matrix
        rank_matrix = []
        for i in range(num_students):
            rank_row = [100 if c=='' else int(c) for c in ws.row_values(i+2,start_colx=
                    9,end_colx=None)]
            rank_matrix.append(rank_row)

        data = Data_b(rank_matrix, seminar_list)
        solution = solve(data)
    
    # Initialize the Excel workbook and sheet
    sb = xlwt.Workbook(encoding = "utf-8")
    s1 = sb.add_sheet("Results")

    s1.write(0,0,"Student")
    s1.write(0,1,"Seminar")
    s1.write(0,2,"Original Ranking")

    for i in range(len(solution)):
        s1.write(i+1,0,solution[i][0])
        s1.write(i+1,1,solution[i][1])
        s1.write(i+1,2,solution[i][2])

    sb.save(filename+"_results.xls")
    # test()


if __name__ == '__main__':
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
    parser.add_argument('filename',help="Input filename")
    logger = logging.getLogger(__name__)
    args = parser.parse_args()    
    logging.basicConfig(format='    %(message)s',level=args.loglevel)

    main(args.filename)
