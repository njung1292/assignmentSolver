import random
import logging
from data_b import Data_b

MIN_ORD = 97

def make_data(num_students, num_seminars):
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
    rank_matrix = [[]]*num_students
    num_fall   = len(fall_list)
    num_spring = len(spring_list)
    seminar_size = num_students / num_seminars
    num_extra = num_students % num_seminars
    for i in range(num_students):
        row = [100]*num_seminars
        top_five = []

        # fall semester
        assert num_fall > 3
        f1, f2, r1 = random.sample(range(num_fall), 3)
        top_five.append(f1)
        top_five.append(f2)

        # spring semester
        assert num_spring > 2
        s1, s2 = random.sample(range(num_fall, num_fall + num_spring), 2)
        top_five.append(s1)
        top_five.append(s2)

        # last seminar
        last_sem = r1 if (r1%2 == 0) else (r1 + num_fall - 1)
        assert last_sem < num_seminars
        top_five.append(last_sem)
        
        random.shuffle(top_five)

        for j in range(5): # We are guaranteed to need to check 5
            row[top_five[j]] = j+1
        rank_matrix[i] = row

    return Data_b(rank_matrix, fall_list + spring_list)
