# from puzzlegame_setup import *
from puzzlegame_setup import NUM_OF_ROWS, NUM_OF_COLUMNS, all_pos, piece_nums, all_pieces, empty_num


class Positions:
    # game's starting position:
    initial_positions = ((4, 0), (3, 1), (3, 2), (4, 3), (0, 0), (2, 0), (0, 3), (2, 3), (2, 1), (0, 1))
    initial_empties = ((4, 1), (4, 2))
    PIECE_NUM = len(initial_positions)

    def __init__(self, pieces = initial_positions, stepnum = 0, dist_to_end = -1, pos_id = 0, neighbors = None):
        self.pieces = pieces
        self.stepnum = stepnum
        #self.empties = self.set_empties()
        self.distance_to_end = dist_to_end
        self.pos_id = pos_id
        # is this check necessary?
        # if self.pieces == self.initial_positions:
        #     self.pos_id = 0
        if neighbors is None:
            self.neighbors = set()
        else:
            self.neighbors = neighbors
        

    def solved(self):
        if self.pieces[-1] == (3, 1):
            self.distance_to_end = 0
            return True
        if self.distance_to_end == 0:
            self.distance_to_end = -1
        return False

    def pieces_cover(self):
        cover = set()
        for j, dimensions in enumerate(all_pieces):
        # for j in range(piece_num):
            y0, x0 = self.pieces[j]
            for y in range(dimensions[0]):
                for x in range(dimensions[1]):
                    cover.add((y0 + y, x0 + x))
        return cover

    def set_empties(self):
        empties = set()
        cover = self.pieces_cover()
        for z in all_pos:
            if z not in cover:
                empties.add(z)
            if len(empties) == empty_num:
                return empties
        return empties

    def reflect(self):
        piece_pos = []
        for j, dimensions in enumerate(all_pieces):
        # for j in range(piece_num):
            y, x = self.pieces[j]
            # x = self.pieces[j][1]
            if dimensions[1] == 1:
                piece_pos.append((y, 3-x))
            if dimensions[1] == 2:
                piece_pos.append((y, 2-x))
        return tuple(piece_pos)
        # no need to create a new Positions object, since reflected object will be equal
        # return Positions(tuple(piece_pos), self.stepnum, self.distance_to_end)

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
                if self.pieces[i] in other_r[i0:i1] and continue_r:
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

    # checking validity of moves
    def move_left_ok(self, piece_id):
        y, x = self.pieces[piece_id]
        if x < 1:
            return False
        height = all_pieces[piece_id][0]
        cover = self.pieces_cover()
        for i in range(height):
            if (y+i, x-1) in cover:
                return False
        return True

    def move_right_ok(self, piece_id):
        y, x = self.pieces[piece_id]
        width = all_pieces[piece_id][1]
        if x >= NUM_OF_COLUMNS - width:
            return False
        height = all_pieces[piece_id][0]
        cover = self.pieces_cover()
        for i in range(height):
            if (y+i, x+width) in cover:
                return False
        return True

    def move_up_ok(self, piece_id):
        y, x = self.pieces[piece_id]
        if y < 1:
            return False
        width = all_pieces[piece_id][1]
        cover = self.pieces_cover()
        for i in range(width):
            if (y-1, x+i) in cover:
                return False
        return True

    def move_down_ok(self, piece_id):
        y, x = self.pieces[piece_id]
        height = all_pieces[piece_id][0]
        if y >= NUM_OF_ROWS - height:
            return False
        width = all_pieces[piece_id][1]
        cover = self.pieces_cover()
        for i in range(width):
            if (y + height, x + i) in cover:
                return False
        return True


    def move_ok(self, move):
        if move < 0 or move >= Positions.PIECE_NUM * 4:
            return False
        if move % 4 == 0: # move.direction == "left":
            return self.move_left_ok(move//4)
        if move % 4 == 1: # move.direction == "right":
            return self.move_right_ok(move // 4)
        if move % 4 == 2: # move.direction == "up":
            return self.move_up_ok(move // 4)
        if move % 4 == 3: # move.direction == "down":
            return self.move_down_ok(move // 4)
        # if something strange happens, can't go anywhere
        return False


    # this doesn't check if the move can be made
    # I don't think the going_fwd variable does anything, so REMOVE???
    def make_move(self, move, going_fwd = True):
        # do we need to check for null move??
        # if move == -1:
        #    return pos
        new_pos = list(self.pieces)
        piece_id = move // 4
        y = self.pieces[piece_id][0]
        x = self.pieces[piece_id][1]
        if move % 4 == 0: # move.direction == "left":
            new_pos[piece_id] = (y, x - 1)
        if move % 4 == 1: # move.direction == "right":
            new_pos[piece_id] = (y, x + 1)
        if move % 4 == 2: # move.direction == "up":
            new_pos[piece_id] = (y - 1, x)
        if move % 4 == 3: # move.direction == "down":
            new_pos[piece_id] = (y + 1, x)
        # bizarre directions don't matter, hopefully
        #if not(move.direction in directions):
            #return pos
        if going_fwd:
            next_pos = Positions(tuple(new_pos), self.stepnum + 1, -1)
        else:
            dist_to_end = -1
            if self.distance_to_end > -1:
                dist_to_end = self.distance_to_end + 1
            next_pos = Positions(tuple(new_pos), self.stepnum, dist_to_end)
        # is more complicated check for distance_to_end needed??
        next_pos.solved()
        return next_pos

    def move_from_coord(self, piece_id, to_coord):
        for move in range(piece_id*4, piece_id*4+4):
            if self.move_ok(move):
                # next_pos = make_move(move, pos)
                if to_coord in self.make_move(move).pieces_cover():
                    return move
        # if no move was found, return -1 (null move)
        return -1
