''' 
Script to generate the file all_pos_13011.py
with all positions and their distances to end,
also generates the file end_positions_484.py
'''

import puzzlesolver as ps

ps.generate_pos_files()

ps.generate_soln_from_all_pos()
