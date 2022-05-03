from pathlib import Path

import pytest

import fix_imports

import position_lists as pl


@pytest.fixture(scope='module')
def pos0():
    return pl.Positions()

@pytest.fixture(scope='module')
def pos1(pos0):
    return pos0.make_move(1)


def test_pos1(pos1):
    assert pos1.move_ok(23)


@pytest.fixture(scope='module')
def pos2(pos1):
    return pos1.make_move(23)

# @pytest.fixture(scope='module')
# def pos_list0(pos0, pos1, pos2):
#     return [pos0, pos1, pos2]

@pytest.fixture(scope='module')
def filepath():
    filename = 'test_pos_list'
    path = Path(__file__).parent / f'{filename}.py'
    yield path
    if path.exists():
        path.unlink()


@pytest.mark.parametrize(
    'move', [1, 7, 11, 12]
)
def test_move_list_from_pos_list(pos0, move):
    pos_list = [pos0, pos0.make_move(move)]
    assert pl.move_list_from_pos_list(pos_list) == [move]


def test_fix_pos_list(pos0, pos1, pos2):
    messed_up_pos_list = [pos0, pl.Positions(pos1.reflect()), pl.Positions(pos2.reflect())]
    for pos in messed_up_pos_list:
        assert isinstance(pos, pl.Positions)
    fixed_pos_list = pl.fix_pos_list(messed_up_pos_list)
    for pos, pos_f in zip([pos0, pos1, pos2], fixed_pos_list):
        assert pos == pos_f
        assert pos.stepnum == pos_f.stepnum
        assert pos.pieces == pos_f.pieces


def test_combine_lists(pos0, pos1, pos2):
    list1 = [pos0, pos1]
    list2 = [pl.Positions(pos1.reflect()), pl.Positions(pos2.reflect())]
    whole_list = pl.combine_lists(list1, list2)
    for pos, pos_l in zip([pos0, pos1, pos2], whole_list):
        assert pos == pos_l
        assert pos.stepnum == pos_l.stepnum
        assert pos.pieces == pos_l.pieces


def test_write_pos_list_to_file(pos0, pos1, pos2, filepath):
    pos_list = [pos0, pos1, pos2]
    pl.write_pos_list_to_file(pos_list, filepath)
    # import the py file we just created
    import test_pos_list as tpl
    for pos, pos_f in zip(pos_list, tpl.pos_list):
        assert pos == pos_f
        assert pos.stepnum == pos_f.stepnum
        assert pos.pieces == pos_f.pieces
        assert pos.distance_to_end == pos_f.distance_to_end
        assert pos.pos_id == pos_f.pos_id
        assert pos.neighbors == pos_f.neighbors
