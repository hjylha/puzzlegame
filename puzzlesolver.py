# from puzzlegame_setup import piece_num
from positions import Positions
import position_lists as pl
# from position_lists import fix_pos_list, write_pos_list_to_file

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
                # print("wrong length")
                return False
        except AttributeError:
            # print("bad content")
            return False
        return True
    except ModuleNotFoundError:
        # print("file not found")
        return False

# then we can just solve the problem
def solve_opt_w_fd(pos):
    if not(does_all_pos_file_exist()):
        # if data does not exist, return False for failure
        return [[pos], False]
    import all_pos_13011
    all_pos = all_pos_13011.pos_list
    i_0 = all_pos.index(pos)
    dist_to_end = all_pos[i_0].stepnum
    if dist_to_end == 0:
        return [[pos], True]
    test_pos = []
    for i in range(dist_to_end):
        # test_pos.append(pos_with_stepnum(i, all_pos))
        test_pos.append([p for p in all_pos if p.stepnum == i])
    # del all_pos[i_0:]
    pos_list = [pos]
    for i in range(dist_to_end):
        for move in range(pos.piece_num * 4):
            if pos_list[i].move_ok(move):
                next_pos = pos_list[i].make_move(move)
                if next_pos in test_pos[dist_to_end-i-1]:
                    pos_list.append(next_pos)
                    break
    return [pos_list, True]

def solve_opt_w_db(pos):
    import db_functions
    # checking database
    if db_functions.does_db_exist():
        pass
        # if not(db_functions.check_pos_db()):
        #     return False
    else:
        return False
    # actually solving problems
    all_pos = db_functions.load_pos_list_from_db()
    i_0 = all_pos.index(pos)
    dist_to_end = all_pos[i_0].distance_to_end
    print(dist_to_end)
    print(len([p for p in all_pos if p.distance_to_end == 0]))
    if dist_to_end == 0:
        return [pos]
    test_pos = []
    for i in range(dist_to_end):
        test_pos.append([p for p in all_pos if p.distance_to_end == i])
    # del all_pos[i_0:]
    pos_list = [pos]
    for i in range(dist_to_end):
        # moved = False
        for move in range(pos.piece_num * 4):
            if pos_list[i].move_ok(move):
                next_pos = pos_list[i].make_move(move)
                if next_pos in test_pos[dist_to_end-i-1]:
                    pos_list.append(next_pos)
                    # moved = True
                    break
        # print(i, moved)
    return pos_list

def find_soln_from_start():
    import db_functions
    # checking database
    if db_functions.does_db_exist():
        pass
        # if not(db_functions.check_pos_db()):
        #     return False
    else:
        return False
    # actually solving problems
    all_pos = db_functions.load_pos_list_from_db()
    pos_list = [pos for pos in all_pos if pos.stepnum == 0]
    while not pos_list[-1].solved():
        for move in range(pos_list[-1].piece_num * 4):
            if pos_list[-1].move_ok(move):
                next_pos = pos_list[-1].make_move(move)
                i0 = all_pos.index(next_pos)
                if all_pos[i0].distance_to_end < pos_list[-1].distance_to_end:
                    pos_list.append(all_pos[i0])
    return pos_list

# IF DATA DOES NOT EXIST, MAKE IT EXIST!!
# find all the end positions
def find_end_positions(starting_positions):
    all_pos = [starting_positions]
    end_pos = []
    active_pos = [starting_positions]
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(pos.piece_num * 4):
                if pos.move_ok(move):
                    next_pos = pos.make_move(move)
                    if not(next_pos in all_pos):
                        all_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
                        if next_pos.solved():
                            end_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
    return end_pos

# find all positions and their stepnum
# hopefully also distance_to_end for positions for which it should be 0
def find_all_positions():
    all_pos = [Positions()]
    active_pos = [Positions()]
    num_of_end_pos = 0
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(pos.piece_num * 4):
                if pos.move_ok(move):
                    next_pos = pos.make_move(move)
                    if not(next_pos in all_pos):
                        all_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
                        if next_pos.solved():
                            num_of_end_pos += 1
                            if not pos.solved():
                                pos.distance_to_end = 1
                            # print(all_pos[-1].distance_to_end)
        active_pos = updated_active_pos.copy()
    print(len(all_pos), "positions found")
    print(num_of_end_pos, "end positions found")
    end_pos = [pos for pos in all_pos if pos.distance_to_end == 0]
    print(len(end_pos), "positions with distance to end equal 0")
    bad_pos = [pos for pos in all_pos if pos.distance_to_end == -1]
    print(len(bad_pos), "positions with undefined distance to end")
    return all_pos

# find all positions and calculate their distance (stepnum) from a given pos_list
def distance_to_pos_list(pos_list):
    for pos in pos_list:
        pos.stepnum = 0
    reached_pos = pos_list.copy()
    active_pos = pos_list.copy()
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(pos.piece_num * 4):
                if pos.move_ok(move):
                    next_pos = pos.make_move(move)
                    if not(next_pos in reached_pos):
                        reached_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
    return reached_pos

def generate_pos_files():
    # generate end positions and write them to file "end_positions_484.py"
    # is this needed???
    end_positions = find_end_positions(Positions())
    # write_pos_list_to_file(end_positions, "end_positions")
    # filename1 = "end_positions_" + str(len(end_positions)) + ".py"
    # print(len(end_positions), "end positions found and written to file " + filename1)
    # generate all positions with their distance (stepnum) from end positions and write to "all_pos_13011.py"
    all_pos = distance_to_pos_list(end_positions)
    for pos in all_pos:
        pos.solved()
    pl.write_pos_list_to_file(all_pos, "all_pos")
    filename2 = "all_pos_" + str(len(all_pos)) + ".py"
    print(len(all_pos), "positions with distances to end found and written to file " + filename2)

# Create a database containing all positions and their distance from end positions
def generate_pos_db():
    import db_functions
    if not db_functions.does_db_exist():
        db_functions.create_pos_db()
    else:
        db_functions.reset_pos_db()
    all_pos = find_all_positions()
    end_pos = [pos for pos in all_pos if pos.distance_to_end == 0]
    print(len(end_pos), "end positions found with the find_all_pos function")
    # end positions should have distance_to_end = 0, so turn to distance 1
    d = 1
    active_pos = list(filter(lambda pos: pos.distance_to_end == d, all_pos))
    while not(active_pos == []):
        updated_active_pos = []
        d += 1
        for pos in active_pos:
            for move in range(pos.piece_num * 4):
                if pos.move_ok(move):
                    current_pos = pos.make_move(move, False)
                    i0 = all_pos.index(current_pos)
                    if all_pos[i0].distance_to_end == -1:
                        all_pos[i0].distance_to_end = d
                        updated_active_pos.append(all_pos[i0])
        active_pos = updated_active_pos.copy()
    db_functions.save_pos_list_to_db(all_pos)
    print(len(all_pos), "positions found and saved to database")
    print(db_functions.check_pos_db())

def generate_pos_db_v2():
    import db_functions
    if not db_functions.does_db_exist():
        db_functions.create_pos_db()
    else:
        db_functions.reset_pos_db()
    all_pos = pl.explore_the_positions()
    print(len(all_pos), "positions found")
    end_pos = [pos for pos in all_pos if pos.distance_to_end == 0]
    print(len(end_pos), "end positions found with the find_all_pos function")
    db_functions.save_pos_list_to_db(all_pos)
    print(len(all_pos), "positions found and saved to database")
    print(db_functions.check_pos_db())

def generate_pos_files_from_db():
    import db_functions
    all_pos = db_functions.load_pos_list_from_db()
    pl.write_pos_list_to_file(all_pos, "all_pos")
    filename2 = "all_pos_" + str(len(all_pos)) + ".py"
    print(len(all_pos), "positions with distances to end found and written to file " + filename2)

# Finding and saving an optimal solution with a given starting position
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
            for move in range(pos.piece_num * 4):
                if pos.move_ok(move):
                    next_pos = pos.make_move(move)
                    # if next_pos has not been visited
                    if not(next_pos in all_att):
                        all_att.append(next_pos)
                        if next_pos.solved():
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
        # potential_pos = pos_with_stepnum(curr_stepnum, all_att)
        potential_pos = [pos for pos in all_att if pos.stepnum == curr_stepnum]
        for move in range(next_pos.piece_num * 4):
            if next_pos.move_ok(move):
                pos = next_pos.make_move(move)
                if pos in potential_pos:
                    soln_opt.append(pos)
                    print("Found step", curr_stepnum)
                    break
    # remember to reverse the order of soln_opt
    soln_opt.reverse()
    return pl.fix_pos_list(soln_opt)

# use all_pos file to generate an optimal solution
def generate_soln_from_all_pos():
    import all_pos_13011
    all_pos = all_pos_13011.pos_list
    start_pos = Positions()
    num_of_steps = all_pos[all_pos.index(start_pos)].stepnum
    soln = [start_pos]
    for i in range(1, num_of_steps + 1):
        curr_pos = soln[-1]
        # potential_pos = pos_with_stepnum(num_of_steps - i, all_pos)
        potential_pos = [pos for pos in all_pos if pos.stepnum == num_of_steps - i]
        for move in range(4 * curr_pos.piece_num):
            if curr_pos.move_ok(move):
                pos = curr_pos.make_move(move)
                if pos in potential_pos:
                    soln.append(pos)
                    break
    filename = "solution_opt_" + str(len(soln)) + ".py"
    pl.write_pos_list_to_file(soln, "solution_opt")
    print("Optimal solution saved to file " + filename)

def generate_soln():
    soln_opt = find_opt_soln(Positions())
    filename = "solution_opt_" + str(len(soln_opt)) + ".py"
    pl.write_pos_list_to_file(soln_opt, "solution_opt")
    print("Optimal solution saved to file " + filename)

