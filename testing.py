# from puzzlegame_setup import *
# from positions import *
from puzzlegame_setup import initial_positions
from positions import Positions
import puzzlesolver as ps
import puzzlesolver_extra as pse


# reilu 1000 askelta
#solution = ps.solve0(Positions(0, initial_positions))

#solution = ps.solve_opt_0(Positions(0, initial_positions))




#ps.distance_to_solution()
#ps.distance_to_end()
#choose_every_kth_stepnum(5)

# full data paljon nopeampi kuin 1/5 tai 1/10 datasta
#solution = ps.solve_opt_w_fd(Positions(0, initial_positions))
#solution = ps.solve_opt_w_10d(Positions(0, initial_positions))
#solution = ps.solve_opt_w_10d(Positions(0, initial_positions))
# solution = ps.solve_opt_from_scratch(Positions(0, initial_positions))
import time
start_time = time.time()

solution = ps.find_opt_soln(Positions())

end_time = time.time()
elapsed_time = end_time - start_time
hours = elapsed_time // 3600
minutes = (elapsed_time - hours * 3600) // 60
print(elapsed_time, hours, minutes)

print(len(solution))
