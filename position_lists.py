from puzzlegame_setup import piece_num
from positions import Positions


def move_list_from_pos_list(pos_list):
    move_list = []
    for i in range(len(pos_list)-1):
        for move in range(piece_num * 4):
            if pos_list[i+1].pieces == pos_list[i].make_move(move).pieces:
                move_list.append(move)
                break
    return move_list


def fix_pos_list(pos_list):
    if len(pos_list) == 1:
        return pos_list
    for i in range(1, len(pos_list)):
        moved = False
        for move in range(piece_num * 4):
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
        pos_list.append(Positions(i, coord_list[i]))
    return pos_list

# combining lists of coordinates
def combine_lists_of_coords(list1, list2):
    if not(list1[-1] == list2[0]):
        print("not valid lists")
        return list1
    coord_list = list1[:]
    return coord_list.extend(list2[1:])


# find the pos with the given stepnum from a pos_list
# list or set? does it matter?
def pos_with_stepnum(num, pos_list):
    pos_list_s = []
    for pos in pos_list:
        if pos.stepnum == num:
            pos_list_s.append(pos)
    return pos_list_s

# functions for saving positions to file
def write_pos_list_to_file(pos_list, filename):
    l = len(pos_list)
    name = filename + "_" + str(l) + ".py"
    file = open(name, "w")
    file.write("from positions import Positions\n\n")
    file.write("pos_list = []\n")
    for i in range(l):
        file.write("pos_list.append(Positions(" + str(pos_list[i].stepnum))
        file.write(", " + str(pos_list[i].pieces) + "))\n")
    file.close()

# not sure about this one
# def write_pos_set_to_file(pos_set, filename):
#     l = len(pos_set)
#     name = filename + "_" + str(l) + ".py"
#     file = open(name, "w")
#     file.write("from positions import Positions\n\n")
#     file.write("pos_set = set()\n")
#     for pos in pos_set:
#         file.write("pos_set.add(Positions(" + str(pos.stepnum))
#         file.write(", " + str(pos.pieces) + "))\n")
#     file.close()
