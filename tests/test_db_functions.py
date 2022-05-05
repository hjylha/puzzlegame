from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

import fix_imports

import db_functions as dbf


@pytest.fixture(scope='module')
def db_path():
    path = Path(__file__).parent / 'test_db.db'
    yield path
    if path.exists():
        path.unlink()


@pytest.fixture(scope='class')
def monkeymodule():
    mp = MonkeyPatch()
    yield mp
    # request.addfinalizer(mp.undo)
    # return mp
    mp.undo()




# @pytest.fixture(scope='module')
# def db(db_path):
#     dbf.sqlite3.connect(db_path)
#     if db_path.exists():
#         db_path.unlink()

class TestDB:

    def test_db_setup(self, monkeymodule, db_path):
        monkeymodule.setattr('db_functions.DB_FILEPATH', db_path)
        assert dbf.DB_FILEPATH.parent == Path(__file__).parent

    def test_create_pos_db(self, db_path):
        assert not db_path.exists()
        dbf.create_pos_db()
        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'SELECT * FROM {dbf.POSITIONS_TABLE_NAME}')
            stuff = c.fetchall()
        assert stuff == []

    def test_reset_pos_db(self, db_path):
        dbf.reset_pos_db()


class TestTransforms:

    @pytest.mark.parametrize(
        ('coord', 'num'), [
            ((0, 0), 0),
            ((4, 0), 4),
            ((0, 3), 15),
            ((3, 1), 8)
        ]
    )
    def test_coord_as_int(self, coord, num):
        assert dbf.coord_as_int(coord) == num

    @pytest.mark.parametrize(
        ('coord', 'num'), [
            ((0, 0), 0),
            ((4, 0), 4),
            ((0, 3), 15),
            ((3, 1), 8)
        ]
    )
    def test_int_as_coord(self, coord, num):
        assert dbf.int_as_coord(num) == coord

    @pytest.mark.parametrize(
        ('pos_tuple', 'tuple_str'), [
            (dbf.Positions.initial_positions, '4,8,13,19,0,2,15,17,7,5'),
            (((1, 2), (4, 1), (3, 3)), '11,9,18')
        ]
    )
    def test_change_pos_tuple_to_string(self, pos_tuple, tuple_str):
        assert dbf.change_pos_tuple_to_string(pos_tuple) == tuple_str

    @pytest.mark.parametrize(
        ('pos_tuple', 'tuple_str'), [
            (dbf.Positions.initial_positions, '4,8,13,19,0,2,15,17,7,5'),
            (((1, 2), (4, 1), (3, 3)), '11,9,18')
        ]
    )
    def test_change_pos_string_to_tuple(self, pos_tuple, tuple_str):
        dbf.change_pos_string_to_tuple(tuple_str) == pos_tuple
    
    @pytest.mark.parametrize(
        ('int_set', 'set_str'), [
            ({1, 2, 3, 4}, '1,2,3,4'),
            ({-1, 52, 156, 13011}, '-1,52,156,13011')
        ]
    )
    def test_change_neighbor_string_to_set(self, int_set, set_str):
        assert dbf.change_neighbor_string_to_set(set_str) == int_set

    @pytest.mark.parametrize(
        'int_set', [
            {1, 2, 3, 4},
            {-1, 52, 156, 13011},
        ]
    )
    def test_change_int_set_to_string(self, int_set):
        int_set_as_str = dbf.change_int_set_to_string(int_set)
        assert isinstance(int_set_as_str, str)
        # assert dbf.change_int_set_to_string(int_set) == set_str
        assert dbf.change_neighbor_string_to_set(int_set_as_str) == int_set

    
