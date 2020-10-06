''' 
Script to generate the file all_pos_13011.py
with all positions and their distances to end,
also generates the file end_positions_484.py
'''
# add some time measurements
import time
start_time = time.time()

import puzzlesolver as ps

ps.generate_pos_files()

ps.generate_soln_from_all_pos()

# end time
end_time = time.time()
elapsed_time = end_time - start_time
hours = elapsed_time // 3600
minutes = (elapsed_time - hours * 3600) // 60
seconds = (elapsed_time % 60) // 1
print(int(hours), "hours,", int(minutes), "minutes,", int(seconds), "seconds")