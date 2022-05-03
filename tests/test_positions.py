import random
import pytest

import fix_imports

import positions
# from positions import Positions

@pytest.fixture(scope='module')
def pos():
    return positions.Positions()


def test_init_default(pos):
    # pos = positions.Positions()
    assert pos.pieces == positions.Positions.initial_positions
    assert pos.stepnum == 0
    assert pos.distance_to_end == -1
    assert pos.pos_id == 0
    assert pos.neighbors == set()


@pytest.mark.parametrize(
    ('pos_tuple', 'stepnum', 'dist_to_end', 'pos_id', 'neighbors'), [
        ((1, 2, 3), random.randint(-1, 5000), random.randint(-1, 5000), random.randint(-1, 5000), {1, 2, 3}),
        (((3, 1), (4, 2)), random.randint(-1, 5000), random.randint(-1, 5000), random.randint(-1, 5000), {3, 4, 5}),
        (((4, 0), (3, 1)), random.randint(-1, 5000), random.randint(-1, 5000), random.randint(-1, 5000), {-4, 2, 937})
    ]
)
def test_init(pos_tuple, stepnum, dist_to_end, pos_id, neighbors):
    pos = positions.Positions(pos_tuple, stepnum, dist_to_end, pos_id, neighbors)
    assert pos.pieces == pos_tuple
    assert pos.stepnum == stepnum
    assert pos.distance_to_end == dist_to_end
    assert pos.pos_id == pos_id
    assert pos.neighbors == neighbors


def test_solved_default(pos):
    # pos = positions.Positions()
    assert not pos.solved()


def test_solved():
    pass


def test_pieces_cover_default(pos):
    # pos = positions.Positions()
    cover = pos.pieces_cover()
    expected_cover = set((y, x) for y in range(5) for x in range(4) if (y, x) not in ((4, 1), (4, 2)))
    assert cover == expected_cover
    # assert (4, 3) in cover
    # assert (1, 0) in cover
    # assert (1, 2) in cover
    # assert (4, 1) not in cover

def test_pieces_cover():
    pass


def test_set_empties_default(pos):
    # pos = positions.Positions()
    assert pos.set_empties() == set(((4, 1), (4, 2)))

def test_set_empties():
    pass


def test_reflect_default(pos):
    # pos = positions.Positions()
    assert pos.reflect() == ((4, 3), (3, 2), (3, 1), (4, 0), (0, 3), (2, 3), (0, 0), (2, 0), (2, 1), (0, 1))

def test_reflect():
    pass


def test_eq_default(pos):
    # pos = positions.Positions()
    pos2 = positions.Positions(pos.reflect())
    assert pos == pos2

def test_eq():
    pass


@pytest.mark.parametrize(
    'piece_id', list(range(positions.Positions.piece_num))
)
def test_move_left_ok_default(pos, piece_id):
    # pos = positions.Positions()
    if piece_id != 3:
        assert not pos.move_left_ok(piece_id)
    else:
        assert pos.move_left_ok(piece_id)

def test_move_left_ok():
    pass


@pytest.mark.parametrize(
    'piece_id', list(range(positions.Positions.piece_num))
)
def test_move_right_ok_default(pos, piece_id):
    # pos = positions.Positions()
    if piece_id == 0:
        assert pos.move_right_ok(piece_id)
    else:
        assert not pos.move_right_ok(piece_id)

def test_move_right_ok():
    pass


@pytest.mark.parametrize(
    'piece_id', list(range(positions.Positions.piece_num))
)
def test_move_up_ok_default(pos, piece_id):
    # pos = positions.Positions()
    assert not pos.move_up_ok(piece_id)

def test_move_up_ok():
    pass


@pytest.mark.parametrize(
    'piece_id', list(range(positions.Positions.piece_num))
)
def test_move_down_ok_default(pos, piece_id):
    # pos = positions.Positions()
    if piece_id in (1, 2):
        assert pos.move_down_ok(piece_id)
    else:
        assert not pos.move_down_ok(piece_id)

def test_move_down_ok():
    pass


@pytest.mark.parametrize(
    'move', list(range(4 * positions.Positions.piece_num))
)
def test_move_ok_default(pos, move):
    if move in (1, 7, 11, 12):
        assert pos.move_ok(move)
    else:
        assert not pos.move_ok(move)

def test_move_ok():
    pass


@pytest.mark.parametrize(
    'move', [1, 7, 11, 12]
)
def test_make_move_default(pos, move):
    assert pos != pos.make_move(move)

def test_make_move():
    pass


@pytest.mark.parametrize(
    ('piece_id', 'coord'), [(piece, coord) for coord in ((4, 1), (4, 2)) for piece in range(4)]
)
def test_move_from_coord_default(pos, piece_id, coord):
    move = pos.move_from_coord(piece_id, coord)
    possible_moves = [1, 7, 11, 12]

    if (piece_id in (0, 1) and coord == (4, 1)) or (piece_id in (2, 3) and coord == (4, 2)):
        assert move == possible_moves[piece_id]
    else:
        assert move == -1

def test_move_from_coord():
    pass
