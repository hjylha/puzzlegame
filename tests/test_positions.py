import fix_imports

import positions
# from positions import Positions


def test_init():
    pos = positions.Positions()
    assert pos.pieces == positions.Positions.initial_positions
    assert pos.stepnum == 0
    assert pos.distance_to_end == -1
    assert pos.pos_id == 0
    assert pos.neighbors == set()

def test_solved():
    pass

def test_pieces_cover():
    pass

