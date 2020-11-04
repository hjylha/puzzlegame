'''
Script to generate a database of all possible puzzlepiece positions and 
their distances (in moves) to the start and the solved position.
'''

# add some time measurements
import time
start_time = time.time()

import puzzlesolver as ps
ps.generate_pos_db()

# end time
end_time = time.time()
elapsed_time = end_time - start_time
hours = elapsed_time // 3600
minutes = (elapsed_time - hours * 3600) // 60
seconds = (elapsed_time % 60) // 1
print(int(hours), "hours,", int(minutes), "minutes,", int(seconds), "seconds")
