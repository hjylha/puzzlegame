
directions = [ "left", "right", "up", "down" ]
piece_symbols = ["1", "2", "3", "4", "Q", "W", "E", "R", "S", "D"]
piece_colors = ["orange", "green", "yellow", "red"]

# coordinates for 5x4 grid
num_of_rows = 5
num_of_columns = 4
all_pos = []
for y in range(num_of_rows):
    for x in range(num_of_columns):
        all_pos.append([y, x])

# needlessly complicated, only need the size of piece
# class Piece:
#    def __init__(self, type, num, size):
#        self.type = type
#        self.num = num
#        self.size = size
#
#    def area(self):
#        return self.size[0] * self.size[1]

# GENERATING PIECES
# 4 1x1 pieces, 4 2x1 pieces, 1 1x2 piece and 1 2x2 piece
piece_nums = [4, 4, 1, 1]
piece_types = [[1,1], [2,1], [1,2], [2,2]]
def generate_piece_list(piece_nums, piece_types):
    piece_list = []
    for j in range(len(piece_nums)):
        for i in range(piece_nums[j]):
            piece_list.append(piece_types[j])
    return piece_list

# generate num of pieces and empties given piece_list
def set_empty_num(piece_list, num_of_rows, num_of_columns):
    covered = 0
    for piece in piece_list:
        covered += piece[0] * piece[1]
    e_num = num_of_rows * num_of_columns - covered
    return e_num

all_pieces = generate_piece_list(piece_nums, piece_types)
piece_num = len(all_pieces)
empty_num = set_empty_num(all_pieces, num_of_rows, num_of_columns)
# game's starting position:
initial_positions = [[4, 0], [3, 1], [3, 2], [4, 3], [0, 0], [2, 0], [0, 3], [2, 3], [2, 1], [0, 1]]
initial_empties = [[4, 1], [4, 2]]

# Can't remember what this was for
# def what_type_is_this_index(index, piece_list=piece_types):
#    num = 0
#    for piece in piece_list:
#        if index in range(num, num + piece.num):
#            return piece
#        num += piece.num
#    print("invalid index")
#    return
