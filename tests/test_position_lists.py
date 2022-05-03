import pytest

import fix_imports

import position_lists as pl


@pytest.fixture(scope='module')
def pos():
    return pl.Positions()


@pytest.mark.parametrize(
    'move', [1, 7, 11, 12]
)
def test_move_list_from_pos_list(pos, move):
    pos_list = [pos, pos.make_move(move)]
    assert pl.move_list_from_pos_list(pos_list) == [move]


def test_fix_pos_list():
    pass


def test_combine_lists():
    pass

