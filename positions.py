# from puzzlegame_setup import *
from puzzlegame_setup import all_pos, piece_nums, all_pieces, piece_num, empty_num, initial_positions


class Positions:
    def __init__(self, stepnum = 0, pieces = initial_positions):
        self.stepnum = stepnum
        self.pieces = pieces
        #self.empties = self.set_empties()

    def pieces_cover(self):
        cover = []
        for j in range(piece_num):
            y0 = self.pieces[j][0]
            x0 = self.pieces[j][1]
            for y in range(all_pieces[j][0]):
                for x in range(all_pieces[j][1]):
                    cover.append([y0 + y, x0 + x])
        return cover

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
                piece_pos.append([y, 3-x])
            if all_pieces[j][1] == 2:
                piece_pos.append([y, 2-x])
        return Positions(self.stepnum, piece_pos)


def are_pos_same(pos1, pos2):
    pos2r = pos2.reflect()
    # checking both pos2 and pos2 reflected
    continue_n = True
    continue_r = True
    i = 0
    for num in piece_nums:
        i0 = i
        i1 = i0 + num
        for j in range(num):
            found_n = False
            found_r = False
            if pos1.pieces[i] in pos2.pieces[i0:i1] and continue_n:
                found_n = True
            if pos1.pieces[i] in pos2r.pieces[i0:i1] and continue_r:
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
def pos_with_stepnum(num, pos_list):
    pos_list_s = []
    for pos in pos_list:
        if pos.stepnum == num:
            pos_list_s.append(pos)
    return pos_list_s


def index_of_pos_in_list(pos, pos_list):
    for i in range(len(pos_list)):
        if are_pos_same(pos, pos_list[i]):
            return i
    # if pos is not in pos_list return -1
    return -1


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
