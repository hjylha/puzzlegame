
directions = ("left", "right", "up", "down")
piece_symbols = ("1", "2", "3", "4", "Q", "W", "E", "R", "S", "D")
piece_colors = ("orange", "green", "yellow", "red")

# coordinates for 5x4 grid
NUM_OF_ROWS = 5
NUM_OF_COLUMNS = 4
all_pos = tuple((y,x) for y in range(NUM_OF_ROWS) for x in range(NUM_OF_COLUMNS))

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
PIECE_NUM = len(all_pieces)
empty_num = set_empty_num(all_pieces, NUM_OF_ROWS, NUM_OF_COLUMNS)
