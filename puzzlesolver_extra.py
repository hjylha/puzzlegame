from puzzlegame_setup import piece_num
from move import move_ok, make_move, combine_lists
from positions import index_of_pos_in_list, pos_with_stepnum, write_pos_list_to_file

# Find a shortest path solution
def solve_opt_from_scratch(pos):
    from generate_positions import find_end_positions as find_end_positions
    from generate_positions import distance_to_pos_list as distance_to_pos_list
    end_pos = find_end_positions(pos)
    print(len(end_pos), "end positions found")
    all_pos = distance_to_pos_list(end_pos)
    print(len(all_pos), "positions in total")
    i_0 = index_of_pos_in_list(pos, all_pos)
    dist_to_end = all_pos[i_0].stepnum
    if dist_to_end == 0:
        return [pos]
    test_pos = []
    for i in range(dist_to_end):
        test_pos.append(pos_with_stepnum(i, all_pos))
    # del all_pos[i_0:]
    pos_list = [pos]
    for i in range(dist_to_end):
        for move in range(piece_num * 4):
            if move_ok(move, pos_list[i]):
                next_pos = make_move(move, pos_list[i])
                if index_of_pos_in_list(next_pos, test_pos[dist_to_end-i-1]) > -1:
                    pos_list.append(next_pos)
                    break
    print("Optimal solution found")
    return pos_list


# TRYING TO FIND SHORTEST PATH SOLUTION WITH LIMITED DATA

# limiting data from full data (all_pos_13011.py)
def choose_every_kth_stepnum(k):
    try:
        import all_pos_13011
    except ModuleNotFoundError:
        print("Module all_pos_13011.py not found")
        return
    all_pos = all_pos_13011.pos_list
    some_pos = []
    for i in range(127 // k):
        for pos in pos_with_stepnum(i*k, all_pos):
            some_pos.append(pos)
    write_pos_list_to_file(some_pos, "every_" + str(k) + "th_pos")
    return some_pos

# try to reach pos_list with k+ steps
def reach_pos_list_opt(pos, pos_list_ref, k = 1):
    if index_of_pos_in_list(pos, pos_list_ref) > -1:
        return [pos]
    att_pos = [pos]
    active_pos_lists = [[pos]]
    while not(active_pos_lists == []):
        updated_active_pos_lists = []
        for pos_list in active_pos_lists:
            curr_pos = pos_list[-1]
            for move in range(piece_num * 4):
                if move_ok(move, curr_pos):
                    next_pos = make_move(move, curr_pos)
                    if index_of_pos_in_list(next_pos, att_pos) == -1:
                        if len(pos_list) >= k:
                            if index_of_pos_in_list(next_pos, pos_list_ref) > -1:
                                pos_list.append(next_pos)
                                return pos_list
                        att_pos.append(next_pos)
                        updated_active_pos_lists.append(pos_list.copy())
                        updated_active_pos_lists[-1].append(next_pos)
        active_pos_lists = updated_active_pos_lists.copy()

# solution while knowing "every 10th position"
def solve_opt_w_10d(pos):
    if pos.pieces[-1] == [3,1]:
        return [pos]
    import every_10th_pos_1726
    ae_pos = every_10th_pos_1726.pos_list
    if index_of_pos_in_list(pos, ae_pos) > -1:
        dist_to_end = ae_pos[index_of_pos_in_list(pos, ae_pos)].stepnum
        # know_dist_to_end = True
    else:
        pos_list0 = reach_pos_list_opt(pos, ae_pos)
        if pos_list0[-1].pieces[-1] == [3,1]:
            return pos_list0
        dist_to_end = ae_pos[index_of_pos_in_list(pos_list0[-1], ae_pos)].stepnum
        # know_dist_to_end = False
    test_pos = []
    for i in range((dist_to_end - 1) // 10 + 1 ):
        test_pos.append(pos_with_stepnum(10*i, ae_pos))
    pos_list = reach_pos_list_opt(pos, test_pos[-1])
    if pos_list[-1].pieces[-1] == [3,1]:
        return pos_list
    for i in range(len(test_pos)):
        pos_list_ext = reach_pos_list_opt(pos_list[-1], test_pos[len(test_pos)-i-1], 10)
        pos_list = combine_lists(pos_list, pos_list_ext)
    if pos_list[-1].pieces[-1] == [3,1]:
        return pos_list
    pos_list_ext = reach_pos_list_opt(pos_list[-1], test_pos[0], 10)
    return combine_lists(pos_list, pos_list_ext)
    
    
# solution while knowing "every 5th position"
def solve_opt_w_5d(pos):
    if pos.pieces[-1] == [3,1]:
        return [pos]
    import every_5th_pos_2965
    ae_pos = every_5th_pos_2965.pos_list
    if index_of_pos_in_list(pos, ae_pos) > -1:
        dist_to_end = ae_pos[index_of_pos_in_list(pos, ae_pos)].stepnum
        # know_dist_to_end = True
    else:
        pos_list0 = reach_pos_list_opt(pos, ae_pos)
        if pos_list0[-1].pieces[-1] == [3,1]:
            return pos_list0
        dist_to_end = ae_pos[index_of_pos_in_list(pos_list0[-1], ae_pos)].stepnum
        # know_dist_to_end = False
    test_pos = []
    for i in range((dist_to_end - 1) // 5 + 1 ):
        test_pos.append(pos_with_stepnum(5*i, ae_pos))
    pos_list = reach_pos_list_opt(pos, test_pos[-1])
    if pos_list[-1].pieces[-1] == [3,1]:
        return pos_list
    for i in range(len(test_pos)):
        pos_list_ext = reach_pos_list_opt(pos_list[-1], test_pos[len(test_pos)-i-1], 5)
        pos_list = combine_lists(pos_list, pos_list_ext)
    if pos_list[-1].pieces[-1] == [3,1]:
        return pos_list
    pos_list_ext = reach_pos_list_opt(pos_list[-1], test_pos[0], 5)
    return combine_lists(pos_list, pos_list_ext)



def solve0(starting_positions):
    pos_list = [starting_positions]
    att_list = [starting_positions]
    while not(pos_list[-1].pieces[-1] == [3,1]):
        curr_pos = pos_list[-1]
        moved = False
        for move in range(piece_num * 4):
            if move_ok(move, curr_pos):
                next_pos = make_move(move, curr_pos)
                # check if we have been here before: if not, it is a good move
                if index_of_pos_in_list(next_pos, att_list) == -1:
                    pos_list.append(next_pos)
                    att_list.append(next_pos)
                    moved = True
                    break
                # if we have been here before, try the next move
                #else:
                    #move += 1
            #else:
                #move += 1
        # if all possible moves lead to familiar places, go back
        if not(moved):
            if len(pos_list) < 2:
                print("No solution found")
                return pos_list
            else:
                pos_list.pop()
    print("SOLVED!!")
    return pos_list

# assuming that pos_list[0] = reference_solution[0]
def solve_w_history0(pos_list, reference_solution):
    pos_list2 = pos_list.copy()
    pos_list2.reverse()
    # stuff to do, lots of it


def solve_w_ref_1(starting_positions, reference_solution):
    if not (index_of_pos_in_list(starting_positions, reference_solution) == -1):
        i_r = index_of_pos_in_list(starting_positions, reference_solution)
        return combine_lists([starting_positions], reference_solution[i_r:])
    all_att = [starting_positions]
    num_of_moves = 1
    while True:
        # try to reach reference_solution or winning condition
        pos_list = [starting_positions]
        att_list = [starting_positions]
        while True:
            # testing positions num_of_moves away from starting_pos
            if len(pos_list) > num_of_moves:
                pos_list.pop()
            curr_pos = pos_list[-1]
            moved = False
            for move in range(piece_num * 4):
                if move_ok(move, curr_pos):
                    next_pos = make_move(move, curr_pos)
                    if index_of_pos_in_list(next_pos, att_list) == -1:
                        i_a = index_of_pos_in_list(next_pos, all_att)
                        if i_a == -1:
                            pos_list.append(next_pos)
                            if next_pos.pieces[-1] == [3,1]:
                                return pos_list
                            if not(index_of_pos_in_list(next_pos, reference_solution) == -1):
                                i_r = index_of_pos_in_list(next_pos, reference_solution)
                                return combine_lists(pos_list, reference_solution[i_r:])
                            att_list.append(next_pos)
                            all_att.append(next_pos)
                            moved = True
                            break
                        else:
                            if all_att[i_a].stepnum >= next_pos.stepnum:
                                pos_list.append(next_pos)
                                att_list.append(next_pos)
                                all_att[i_a].stepnum = next_pos.stepnum
                                moved = True
                                break
            if not(moved):
                if len(pos_list) < 2:
                    num_of_moves += 1
                    break
                else:
                    pos_list.pop()
                    

def solve_opt_0(starting_positions):
    all_att = [starting_positions]
    active_pos_lists = [[starting_positions]]
    num_of_moves = 1
    while not(active_pos_lists == []):
        updated_active_pos_lists = []
        l = len(active_pos_lists)
        #print(num_of_moves, l, " LOOKING FOR SOLUTIONS!")
        for pos_list in active_pos_lists:
            # not sure what this is for
            # i_p = active_pos_lists.index(pos_list)
            curr_pos = pos_list[-1]
            #print(num_of_moves, i_p, curr_pos.pieces)
            # moved = False
            for move in range(piece_num * 4):
                # m =[curr_pos.pieces[move//4], move//4, move%4]
                if move_ok(move, curr_pos):
                    #print(num_of_moves, i_p, m[0], m[1], m[2], " FOUND A POSSIBLE MOVE!")
                    next_pos = make_move(move, curr_pos)
                    if index_of_pos_in_list(next_pos, all_att) == -1:
                        # if this pos hasn't been reached, go forward
                        #print(num_of_moves, i_p, m[0], m[1], m[2], " BRAND NEW POS FOUND, MOVING FORWARD!")
                        all_att.append(next_pos)
                        if next_pos.pieces[-1] == [3,1]:
                            pos_list.append(next_pos)
                            return pos_list
                        updated_active_pos_lists.append(pos_list.copy())
                        updated_active_pos_lists[-1].append(next_pos)
                        # moved = True
                    else:
                        # has this pos been reached more optimally before?
                        # yes, pretty much by definition
                        i_a = index_of_pos_in_list(next_pos, all_att)
                        if next_pos.stepnum < all_att[i_a].stepnum:
                            #print(num_of_moves, i_p, m[0], m[1], m[2], " MORE OPTIMAL WAY TO REACH OLD POS FOUND!")
                            all_att[i_a].stepnum = next_pos.stepnum
                            #pos_list.append(next_pos)
                            updated_active_pos_lists.append(pos_list.copy())
                            updated_active_pos_lists[-1].append(next_pos)
                            # moved = True
        active_pos_lists = updated_active_pos_lists
        l = len(active_pos_lists)
        print(num_of_moves, l, " NO SOLUTION FOUND YET!")
        num_of_moves += 1


# investigating the space of positions
def distance_to_solution():
    import solution_opt_117
    ref_soln = solution_opt_117.solution_117
    # active_pos_lists = []
    for pos in ref_soln:
        pos.stepnum = 0
        # active_pos_lists.append([pos])
    winning_pos = [ref_soln[-1]]
    pos_reached = ref_soln.copy()
    active_pos = ref_soln.copy()
    num_of_moves = 1
    while not(active_pos == []): # and num_of_moves < 50:
        updated_active_pos = []
        for pos in active_pos:
            for move in range(piece_num * 4):
                if move_ok(move, pos):
                    next_pos = make_move(move, pos)
                    if index_of_pos_in_list(next_pos, pos_reached) == -1:
                        pos_reached.append(next_pos)
                        updated_active_pos.append(next_pos)
                        if next_pos.pieces[-1] == [3,1]:
                            winning_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
        l = len(active_pos)
        l2 = len(winning_pos)
        print(num_of_moves, l, l2, " STILL LOOKING!!")
        num_of_moves += 1
    for pos in winning_pos:
        pos.stepnum = 0
    write_pos_list_to_file(winning_pos, "end_positions")
    write_pos_list_to_file(pos_reached, "all_positions")
    return winning_pos


def distance_to_end():
    import end_positions_484
    reached_pos = end_positions_484.pos_list
    active_pos = reached_pos.copy()
    num_of_moves = 1
    while not(active_pos == []):
        updated_active_pos = []
        for pos in active_pos:
            for move in range(piece_num * 4):
                if move_ok(move, pos):
                    next_pos = make_move(move, pos)
                    if index_of_pos_in_list(next_pos, reached_pos) == -1:
                        reached_pos.append(next_pos)
                        updated_active_pos.append(next_pos)
        active_pos = updated_active_pos.copy()
        num_of_moves += 1
        print(num_of_moves, "FOUND ", len(reached_pos), "POSITIONS SO FAR")
    write_pos_list_to_file(reached_pos, "all_pos")
