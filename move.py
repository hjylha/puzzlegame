from puzzlegame_setup import num_of_rows, num_of_columns, all_pos, piece_nums, all_pieces, piece_num, empty_num, initial_positions
from positions import Positions

# checking validity of moves
def move_left_ok(piece_id, pos):
    y, x = pos.pieces[piece_id]
    if x < 1:
        return False
    height = all_pieces[piece_id][0]
    cover = pos.pieces_cover()
    for i in range(height):
        if (y+i, x-1) in cover:
            return False
    return True

def move_right_ok(piece_id, pos):
    y, x = pos.pieces[piece_id]
    width = all_pieces[piece_id][1]
    if x >= num_of_columns - width:
        return False
    height = all_pieces[piece_id][0]
    cover = pos.pieces_cover()
    for i in range(height):
        if (y+i, x+width) in cover:
            return False
    return True

def move_up_ok(piece_id, pos):
    y, x = pos.pieces[piece_id]
    if y < 1:
        return False
    width = all_pieces[piece_id][1]
    cover = pos.pieces_cover()
    for i in range(width):
        if (y-1, x+i) in cover:
            return False
    return True

def move_down_ok(piece_id, pos):
    y, x = pos.pieces[piece_id]
    height = all_pieces[piece_id][0]
    if y >= num_of_rows - height:
        return False
    width = all_pieces[piece_id][1]
    cover = pos.pieces_cover()
    for i in range(width):
        if (y + height, x + i) in cover:
            return False
    return True


def move_ok(move, pos):
    if move < 0 or move >= piece_num * 4:
        return False
    if move % 4 == 0: # move.direction == "left":
        return move_left_ok(move//4, pos)
    if move % 4 == 1: # move.direction == "right":
        return move_right_ok(move // 4, pos)
    if move % 4 == 2: # move.direction == "up":
        return move_up_ok(move // 4, pos)
    if move % 4 == 3: # move.direction == "down":
        return move_down_ok(move // 4, pos)
    # if something strange happens, can't go anywhere
    return False


# this doesn't check if the move can be made
def make_move(move, pos):
    # do we need to check for null move??
    # if move == -1:
    #    return pos
    new_pos = list(pos.pieces)
    piece_id = move // 4
    y = pos.pieces[piece_id][0]
    x = pos.pieces[piece_id][1]
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
    return Positions(pos.stepnum + 1, tuple(new_pos))


def move_from_coord(piece_id, to_coord, pos):
    for move in range(piece_id*4, piece_id*4+4):
        if move_ok(move, pos):
            # next_pos = make_move(move, pos)
            if to_coord in make_move(move, pos).pieces_cover():
                return move
    # if no move was found, return -1 (null move)
    return -1


def move_list_from_pos_list(pos_list):
    move_list = []
    for i in range(len(pos_list)-1):
        for move in range(piece_num*4):
            if pos_list[i+1].pieces == make_move(move,pos_list[i]).pieces:
                move_list.append(move)
                break
    return move_list


def fix_pos_list(pos_list):
    if len(pos_list) == 1:
        return pos_list
    for i in range(1, len(pos_list)):
        moved = False
        for move in range(piece_num * 4):
            if move_ok(move, pos_list[i-1]):
                possible_pos = make_move(move, pos_list[i-1])
                if pos_list[i] == possible_pos:
                    pos_list[i] = possible_pos
                    moved = True
        if not(moved):
            print("not a valid list of positions")
            return pos_list
    return pos_list


# pos_list[-1] = pos_list2[0]
# should this be checked here ???
def combine_lists(pos_list1, pos_list2):
    pos_list1.extend(pos_list2)
    return fix_pos_list(pos_list1)
