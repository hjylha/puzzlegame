'''
Script to generate a database of all possible puzzlepiece positions and 
their distances (in moves) to the start and the solved position.
'''

from puzzlesolver import generate_pos_db
from db_functions import generate_language_table

def generate_db():
    generate_pos_db()
    generate_language_table()

if __name__ == '__main__':
    # add some time measurements
    # import time
    # start_time = time.time()
    import timeit
    start_time = timeit.default_timer()
    

    generate_db()

    # end time
    # end_time = time.time()
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time - hours * 3600) // 60
    seconds = (elapsed_time % 60) // 1
    print(f"{elapsed_time=}")
    print(int(hours), "hours,", int(minutes), "minutes,", int(seconds), "seconds")
