from positions import Positions


def move_list_from_pos_list(pos_list):
    move_list = []
    for i in range(len(pos_list)-1):
        for move in range(pos_list[i].piece_num * 4):
            if pos_list[i+1].pieces == pos_list[i].make_move(move).pieces:
                move_list.append(move)
                break
    return move_list


def fix_pos_list(pos_list):
    if len(pos_list) == 1:
        return pos_list
    for i in range(1, len(pos_list)):
        moved = False
        for move in range(pos_list[i].piece_num * 4):
            if pos_list[i-1].move_ok(move):
                possible_pos = pos_list[i-1].make_move(move)
                if pos_list[i] == possible_pos:
                    pos_list[i] = possible_pos
                    moved = True
        if not(moved):
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
def write_pos_list_to_file(pos_list, filename):
    l = len(pos_list)
    name = filename + "_" + str(l) + ".py"
    file = open(name, "w")
    file.write("from positions import Positions\n\n")
    file.write("pos_list = []\n")
    for i in range(l):
        file.write("pos_list.append(Positions(" + str(pos_list[i].pieces))
        file.write(", " + str(pos_list[i].stepnum) + ", " + str(pos_list[i].distance_to_end) + "))\n")
        file.write("pos_list[-1].id = " + str(pos_list[i].id) + "\n")
        file.write("pos_list[-1].neighbors = " + str(pos_list[i].neighbors) + "\n")
    file.close()

def explore_the_positions():
    all_pos = [Positions()]
    active_ids = [0]
    id = 1
    while not active_ids == []:
        updated_active_ids = []
        for i in active_ids:
            for move in range(all_pos[i].piece_num * 4):
                if all_pos[i].move_ok(move):
                    next_pos = all_pos[i].make_move(move)
                    if next_pos in all_pos:
                        id0 = all_pos.index(next_pos)
                        if not(id0 in all_pos[i].neighbors):
                            all_pos[i].neighbors.add(id0)
                            all_pos[id0].neighbors.add(i)
                    else:
                        all_pos.append(next_pos)
                        all_pos[-1].id = id
                        all_pos[-1].neighbors.add(i)
                        all_pos[i].neighbors.add(id)
                        updated_active_ids.append(id)
                        if all_pos[-1].solved():
                            if not all_pos[i].solved():
                                all_pos[i].distance_to_end = 1
                        id += 1
        active_ids = updated_active_ids
    checked_ids = [pos.id for pos in all_pos if pos.distance_to_end == 0]
    active_ids = checked_ids
    # dist_to_end = 1
    while not active_ids == []:
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
