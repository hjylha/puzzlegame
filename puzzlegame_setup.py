
directions = ("left", "right", "up", "down")
piece_symbols = ("1", "2", "3", "4", "Q", "W", "E", "R", "S", "D")
piece_colors = ("orange", "green", "yellow", "red")

# coordinates for 5x4 grid
num_of_rows = 5
num_of_columns = 4
all_pos = tuple((y,x) for y in range(num_of_rows) for x in range(num_of_columns))

# GENERATING PIECES
# 4 1x1 pieces, 4 2x1 pieces, 1 1x2 piece and 1 2x2 piece
piece_nums = (4, 4, 1, 1)
piece_types = ((1,1), (2,1), (1,2), (2,2))
def generate_piece_list(piece_nums, piece_types):
    piece_list = tuple(piece_types[j] for j in range(len(piece_nums)) for i in range(piece_nums[j]))
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
