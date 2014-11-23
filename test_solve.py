import solve
import argparse
import logging
from data import Data
from collections import Counter


def test(num_students, num_seminars):
    # data = dataGen.make_data(num_students, num_seminars)
    data = Data.factory(num_students, num_seminars)
    
    solution = solve.solve(data)[0]

    # Verify the class sizes
    seminar_ctr = Counter()
    for decision in solution:
        seminar_ctr[decision[1]] += 1
    sorted_sems = sorted(seminar_ctr.items())
    print "Class sizes: "
    for name, count in sorted_sems:
        print '%s: %d' % (name, count)
    # print [seminar_ctr.items()[i][0] for i in range(num_extra)]
    num_extra = num_students % num_seminars
    popular_seminars = sorted(data.popular_seminars[0:num_extra])
    print "\nAdded seminars (class: popularity):"
    for idx, count in popular_seminars:
        print '%s: %d' % (data.year_list[idx], count)

    # if lvl == 1:
    #     num_students1 = 5
    #     fall_list1    = ['f01', 'f02']
    #     spring_list1  = ['s01', 's02']
    #     names1        = ['A', 'B', 'C', 'D', 'E']
    #     top_fives1    = [['s01', 'f01', 's02'],
    #                     ['s02', 'f02', 'f01'],
    #                     ['f02', 's02', 's01'],
    #                     ['s01', 'f02', 's02'],
    #                     ['f01', 's01', 's02']]

    # elif lvl == 2:
    #     num_students2 = 100
    #     fall_list2    = ['f01','f02','f03','f04','f05']
    #     spring_list2  = ['s01','s02','s03','s04','s05']
    #     dg = DataGen(fall_list2, spring_list2, num_students2)

    # elif lvl == 3:
    #     num_students3 = 350
    #     fall_list3    = ['f01','f02','f03','f04','f05','f06','f07','f08','f09','f10','f11']
    #     spring_list3  = ['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11']

    # if lvl >= 2:
    #     dg       = DataGen(fall_list, spring_list, num_students)
    #     names    = dg.generateNames()
    #     top_fives = dg.generateRanks()

    # data     = Data(names, top_fives, fall_list, spring_list)
    # solution = solve.solve(data)
    # return solution


    # print "  --> Seminar Counts: " + str(seminarCounts.items())

def main(args):
    test(int(args.n), int(args.m))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',
        help    = 'Print lots of debugging statements',
        action  = "store_const",
        dest    = "loglevel",
        const   = logging.DEBUG,
        default = logging.WARNING
    )
    parser.add_argument('-v','--verbose',
        help   = 'Be verbose',
        action = "store_const",
        dest   = "loglevel",
        const  = logging.INFO
    )
    parser.add_argument("n", help="Number of students")
    parser.add_argument("m", help="Number of seminars")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(message)s', level=args.loglevel)

    main(args)
