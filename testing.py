# from puzzlegame_setup import *
# from positions import *
from puzzlegame_setup import initial_positions
from positions import Positions
import puzzlesolver as ps


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
solution = ps.solve_opt_from_scratch(Positions(0, initial_positions))
print(len(solution))
