import random
import logging

MIN_ORD = 97
MAX_ORD = 123

class DataGen:
    """Class that randomly generates data."""

    def __init__(self, num_students, num_seminars):
        """Create a new instance."""
        self.fs = []    # Fall seminar names
        self.ss = []    # Spring seminar names
        self.num_students = num_students
        self.num_seminars = num_seminars

        # Generate a list of fall and spring classes
        for i in range(num_seminars/2):
            self.fs.append("F" + str(i+1))
            self.ss.append("S" + str(i+1))
        if (num_seminars % 2 == 1):
            self.fs.append("F" + str(num_seminars/2 + 1))

    def generate_names(self):
        """Returns a list of unique strings representing student names."""
        logging.info("Generating names...")

        assert self.num_students < 26*26

        names = []
        for i in range(MIN_ORD, MAX_ORD):
            for j in range(MIN_ORD, MAX_ORD):
                names.append(str(unichr(i))+str(unichr(j)))
                if (len(names) == self.num_students):
                    return names

    def generate_top_fives(self):
        """Returns a 2D list of top 5 seminars (int index) for each student."""
        logging.info("Generating random top five rankings...")

        top_fives  = []
        num_fall   = len(self.fs)
        num_spring = len(self.ss)
        for student in range(self.num_students):
            my_list = []

            # fall semester
            assert num_fall > 3
            f1, f2, r1 = random.sample(range(num_fall), 3)
            my_list.append(f1)
            my_list.append(f2)

            # spring semester
            assert num_spring > 2
            s1, s2 = random.sample(range(num_fall, num_fall + num_spring), 2)
            my_list.append(s1)
            my_list.append(s2)

            # last seminar
            last_sem = r1 if (r1%2 == 0) else r1 + num_fall - 1
            assert last_sem < self.num_seminars
            my_list.append(last_sem)
            
            random.shuffle(my_list)
            top_fives.append(my_list)

        return top_fives
