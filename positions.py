# from puzzlegame_setup import *
from puzzlegame_setup import all_pos, piece_nums, all_pieces, piece_num, empty_num


class Positions:
    # game's starting position:
    initial_positions = ((4, 0), (3, 1), (3, 2), (4, 3), (0, 0), (2, 0), (0, 3), (2, 3), (2, 1), (0, 1))
    initial_empties = ((4, 1), (4, 2))
    def __init__(self, stepnum = 0, pieces = initial_positions):
        self.stepnum = stepnum
        self.pieces = pieces
        #self.empties = self.set_empties()

    def solved(self):
        if self.pieces[-1] == (3, 1):
            return True
        return False

    def pieces_cover(self):
        cover = []
        for j in range(piece_num):
            y0 = self.pieces[j][0]
            x0 = self.pieces[j][1]
            for y in range(all_pieces[j][0]):
                for x in range(all_pieces[j][1]):
                    cover.append((y0 + y, x0 + x))
        return tuple(cover)

    def set_empties(self):
        empties = []
        cover = self.pieces_cover()
        for z in all_pos:
            if not(z in cover):
                empties.append(z)
            if len(empties) == empty_num:
                return empties
        return empties

    def reflect(self):
        piece_pos = []
        for j in range(piece_num):
            y = self.pieces[j][0]
            x = self.pieces[j][1]
            if all_pieces[j][1] == 1:
                piece_pos.append((y, 3-x))
            if all_pieces[j][1] == 2:
                piece_pos.append((y, 2-x))
        return Positions(self.stepnum, tuple(piece_pos))

    def __eq__(self, other):
        # equality ignores stepnum, but takes reflection into account
        # maybe this is not the best way to do things??
        other_r = other.reflect()
        continue_n = True
        continue_r = True
        i = 0
        for num in piece_nums:
            i0 = i
            i1 = i0 + num
            for _ in range(num):
                found_n = False
                found_r = False
                if self.pieces[i] in other.pieces[i0:i1] and continue_n:
                    found_n = True
                if self.pieces[i] in other_r.pieces[i0:i1] and continue_r:
                    found_r = True
                # if we found corresponding piece locations, we continue checking
                if found_n or found_r:
                    i += 1
                # otherwise pos1 != pos2
                else:
                    return False
                # if we didn't find corresponding piece location, we don't continue
                if not(found_n):
                    continue_n = False
                if not(found_r):
                    continue_r = False
                if not(continue_n) and not(continue_r):
                    return False
        return True

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
