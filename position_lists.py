
from positions import Positions


def move_list_from_pos_list(pos_list):
    if len(pos_list) == 1:
        return []
    move_list = []
    for i in range(len(pos_list) - 1):
        for move in range(Positions.PIECE_NUM * 4):
            if pos_list[i+1].pieces == pos_list[i].make_move(move).pieces:
                move_list.append(move)
                break
    return move_list


def fix_pos_list(pos_list):
    # if len(pos_list) == 1:
    #     return pos_list
    # for i in range(1, len(pos_list)):
    last = len(pos_list) - 1
    for i, pos in enumerate(pos_list):
        if i == last:
            return pos_list
        for move in range(Positions.PIECE_NUM * 4):
            if pos.move_ok(move):
                possible_pos = pos.make_move(move)
                if pos_list[i+1] == possible_pos:
                    pos_list[i+1] = possible_pos
                    break
        else:
            print("not a valid list of positions")
            return pos_list
    return pos_list


# pos_list1[-1] = pos_list2[0]
# should this be checked here ???
def combine_lists(pos_list1, pos_list2):
    pos_list = pos_list1[:]
    pos_list_2 = [pos_list1[-1]]
    pos_list_2.extend(pos_list2[1:])
    pos_list_2 = fix_pos_list(pos_list_2)
    pos_list.extend(pos_list_2[1:])
    # return fix_pos_list(pos_list)
    return pos_list


# functions for saving positions to file
def write_pos_list_to_file(pos_list, filepath):
    # l = len(pos_list)
    # name = f"{filename}.py"
    # file = open(name, "w")
    with open(filepath, "w") as file:
        file.write("from positions import Positions\n\n")
        file.write("pos_list = []\n")
        # for i in range(l):
        for pos in pos_list:
            file.write(f"pos_list.append(Positions( {str(pos.pieces)}")
            file.write(f", {str(pos.stepnum)}, {str(pos.distance_to_end)}")
            file.write(f", {str(pos.pos_id)}, set({str(pos.neighbors)})))\n")
            # file.write("pos_list[-1].pos_id = " + str(pos_list[i].pos_id) + "\n")
            # file.write("pos_list[-1].neighbors = " + str(pos_list[i].neighbors) + "\n")
    # file.close()

# THE BIG ONE
def explore_the_positions():
    all_pos = [Positions()]
    num_of_moves = Positions.PIECE_NUM * 4
    # active_ids = [0]
    curr_id = 1
    low_index = 0
    next_index = 0
    forward_index = curr_id
    while next_index < forward_index:
        # updated_active_ids = []
        searchable_pos = all_pos[low_index:]
        for i in range(next_index, forward_index):
            for move in range(num_of_moves):
                if all_pos[i].move_ok(move):
                    next_pos = all_pos[i].make_move(move)
                    if next_pos in searchable_pos:
                        id0 = low_index + searchable_pos.index(next_pos)
                        if not(id0 in all_pos[i].neighbors):
                            all_pos[i].neighbors.add(id0)
                            all_pos[id0].neighbors.add(i)
                    else:
                        all_pos.append(next_pos)
                        all_pos[-1].pos_id = curr_id
                        all_pos[-1].neighbors.add(i)
                        all_pos[i].neighbors.add(curr_id)
                        # updated_active_ids.append(curr_id)
                        if all_pos[-1].solved():
                            if not all_pos[i].solved():
                                all_pos[i].distance_to_end = 1
                        curr_id += 1
                        searchable_pos.append(next_pos)
        # active_ids = updated_active_ids
        low_index = next_index
        next_index = forward_index
        forward_index = curr_id
    checked_ids = [pos.pos_id for pos in all_pos if pos.distance_to_end == 0]
    active_ids = checked_ids
    # dist_to_end = 1
    while active_ids:
        updated_active_ids = []
        for i in active_ids:
            for j in all_pos[i].neighbors:
                if not j in checked_ids:
                    all_pos[j].distance_to_end = all_pos[i].distance_to_end + 1
                    updated_active_ids.append(j)
                    checked_ids.append(j)
        active_ids = updated_active_ids
    return all_pos


# THE REST MIGHT NOT BE NEEDED!!!!!
# turning list of positions into a list of coordinates
def simplify_pos_list(pos_list):
    pos_list_to_return = []
    for pos in pos_list:
        pos_list_to_return.append(pos.pieces)
    return pos_list_to_return

# the other way around: coordinates into positions
def into_pos_list(coord_list):
    pos_list = []
    for i in range(len(coord_list)):
        pos_list.append(Positions(coord_list[i], i))
    return pos_list

# combining lists of coordinates
def combine_lists_of_coords(list1, list2):
    if not(list1[-1] == list2[0]):
        print("not valid lists")
        return list1
    coord_list = list1[:]
    return coord_list.extend(list2[1:])
