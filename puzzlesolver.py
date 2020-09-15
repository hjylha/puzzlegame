from puzzlegame_setup import piece_num, initial_positions
from positions import Positions, pos_with_stepnum, write_pos_list_to_file
# from positions import index_of_pos_in_list
from move import move_ok, make_move, fix_pos_list

''' 
    let's use big knowledge 
    (aka full data: distance to end for all positions in file "all_pos_13011.py")
    to solve problems
'''
# check if the file "all_pos_13011.py" already exists
def does_all_pos_file_exist():
    try:
        import all_pos_13011
        # check that the file contains all positions
        try:
            all_pos = all_pos_13011.pos_list
            if len(all_pos) != 13011:
                return False
            return True
        except AttributeError:
            return False
    except ModuleNotFoundError:
        return False

# check the file "solution_opt_117.py" for later
def does_soln_117_file_exist():
    try:
        import solution_opt_117
        try:
            soln = solution_opt_117.pos_list
            if len(soln) != 117:
                print("wrong length")
                return False
        except AttributeError:
            print("bad content")
            return False
        return True
    except ModuleNotFoundError:
        print("file not found")
        return False

# then we can just solve the problem
def solve_opt_w_fd(pos):
    if not(does_all_pos_file_exist()):
        # if data does not exist, return False for failure
        return [[pos], False]
    import all_pos_13011
    all_pos = all_pos_13011.pos_list
    # i_0 = index_of_pos_in_list(pos, all_pos)
    i_0 = all_pos.index(pos)
    dist_to_end = all_pos[i_0].stepnum
    if dist_to_end == 0:
        return [[pos], True]
    test_pos = []
    for i in range(dist_to_end):
        test_pos.append(pos_with_stepnum(i, all_pos))
    # del all_pos[i_0:]
    pos_list = [pos]
    for i in range(dist_to_end):
        for move in range(piece_num * 4):
            if move_ok(move, pos_list[i]):
                next_pos = make_move(move, pos_list[i])
                # if index_of_pos_in_list(next_pos, test_pos[dist_to_end-i-1]) > -1:
                if next_pos in test_pos[dist_to_end-i-1]:
                    pos_list.append(next_pos)
                    break
    return [pos_list, True]

# IF DATA DOES NOT EXIST, MAKE IT EXIST!!
# find all the end positions
def find_end_positions(starting_positions):
    all_pos = [starting_positions]
    end_pos = []
    active_pos = [starting_positions]
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(piece_num * 4):
                if move_ok(move, pos):
                    next_pos = make_move(move, pos)
                    # if index_of_pos_in_list(next_pos, all_pos) == -1:
                    if not(next_pos in all_pos):
                        all_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
                        if next_pos.pieces[-1] == [3,1]:
                            end_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
    # print(len(end_pos), "end positions found")
    return end_pos

# find all positions and calculate their distance (stepnum) from a given pos_list
def distance_to_pos_list(pos_list):
    for pos in pos_list:
        pos.stepnum = 0
    reached_pos = pos_list.copy()
    active_pos = pos_list.copy()
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(piece_num * 4):
                if move_ok(move, pos):
                    next_pos = make_move(move, pos)
                    # if index_of_pos_in_list(next_pos, reached_pos) == -1:
                    if not(next_pos in reached_pos):
                        reached_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
    # print(len(reached_pos), "positions with distances found")
    return reached_pos

def generate_pos_files():
    # generate end positions and write them to file "end_positions_484.py"
    end_positions = find_end_positions(Positions(0, initial_positions))
    write_pos_list_to_file(end_positions, "end_positions")
    filename1 = "end_positions_" + str(len(end_positions)) + ".py"
    print(len(end_positions), "end positions found and written to file " + filename1)
    # generate all positions with their distance (stepnum) from end positions and write to "all_pos_13011.py"
    all_pos = distance_to_pos_list(end_positions)
    write_pos_list_to_file(all_pos, "all_pos")
    filename2 = "all_pos_" + str(len(all_pos)) + ".py"
    print(len(all_pos), "positions with distances to end found and written to file " + filename2)

# Finding and saving an optimal solution with default starting position
def find_opt_soln(starting_pos):
    all_att = [starting_pos]
    latest_pos = [starting_pos]
    soln_opt = []
    # first try to find the end
    found_the_end = False
    # num_of_steps_taken = 1
    while not(found_the_end):
        updated_latest_pos = []
        for pos in latest_pos:
            for move in range(piece_num * 4):
                if move_ok(move, pos):
                    next_pos = make_move(move, pos)
                    # if next_pos has not been visited
                    if not(next_pos in all_att):
                        all_att.append(next_pos)
                        if next_pos.pieces[-1] == [3,1]:
                            num_of_steps = next_pos.stepnum
                            print(num_of_steps, "steps in solution")
                            soln_opt.append(next_pos)
                            soln_opt.append(pos)
                            found_the_end = True
                        updated_latest_pos.append(next_pos)
        latest_pos = updated_latest_pos
        # print(num_of_steps_taken, len(latest_pos))
        # num_of_steps_taken += 1
    # backtracking to the start using the all_att
    for i in range(1, num_of_steps):
        curr_stepnum = num_of_steps - i - 1
        next_pos = soln_opt[-1]
        potential_pos = pos_with_stepnum(curr_stepnum, all_att)
        for move in range(piece_num * 4):
            if move_ok(move, next_pos):
                pos = make_move(move, next_pos)
                if pos in potential_pos:
                    soln_opt.append(pos)
                    print("Found step", curr_stepnum)
                    break
    # remember to reverse the order of soln_opt
    soln_opt.reverse()
    return fix_pos_list(soln_opt)

# use all_pos file to generate an optimal solution
def generate_soln_from_all_pos():
    import all_pos_13011
    all_pos = all_pos_13011.pos_list
    start_pos = Positions()
    num_of_steps = all_pos[all_pos.index(start_pos)].stepnum
    soln = [start_pos]
    for i in range(1, num_of_steps + 1):
        curr_pos = soln[-1]
        potential_pos = pos_with_stepnum(num_of_steps - i, all_pos)
        for move in range(4 * piece_num):
            if move_ok(move, curr_pos):
                pos = make_move(move, curr_pos)
                if pos in potential_pos:
                    soln.append(pos)
                    break
    filename = "solution_opt_" + str(len(soln)) + ".py"
    write_pos_list_to_file(soln, "solution_opt")
    print("Optimal solution saved to file " + filename)

def generate_soln():
    soln_opt = find_opt_soln(Positions())
    filename = "solution_opt_" + str(len(soln_opt)) + ".py"
    write_pos_list_to_file(soln_opt, "solution_opt")
    print("Optimal solution saved to file " + filename)

