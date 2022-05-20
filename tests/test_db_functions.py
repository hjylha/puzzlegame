from email.policy import default
from pathlib import Path
from random import randint

import pytest
from _pytest.monkeypatch import MonkeyPatch

import fix_imports

import db_functions as dbf


@pytest.fixture(scope='module')
def db_path():
    path = Path(__file__).parent / 'test_db.db'
    # maybe something went wrong before
    if path.exists():
        path.unlink()
    yield path
    # delete the file if it exists after testing
    if path.exists():
        path.unlink()


@pytest.fixture(scope='class')
def monkeymodule():
    mp = MonkeyPatch()
    yield mp
    # request.addfinalizer(mp.undo)
    # return mp
    mp.undo()


@pytest.fixture(scope='module')
def pos_list0():
    pos_list = [dbf.Positions()]
    for move in range(4* dbf.Positions.PIECE_NUM):
        if pos_list[0].move_ok(move):
            pos_list.append(pos_list[0].make_move(move))
            pos_list[-1].pos_id = len(pos_list) - 1
    return pos_list


@pytest.fixture(scope='module')
def languages():
    return ('ENG', 'SWE')


# @pytest.fixture(scope='module')
# def db(db_path):
#     dbf.sqlite3.connect(db_path)
#     if db_path.exists():
#         db_path.unlink()

class TestDB:

    def test_db_setup(self, monkeymodule, db_path):
        monkeymodule.setattr('db_functions.DB_FILEPATH', db_path)
        assert dbf.DB_FILEPATH.parent == Path(__file__).parent
    
    def test_does_db_exist(self, db_path):
        # first the file does not exist
        assert not dbf.does_db_exist()
        # if the file exists, but is not db
        with open(db_path, 'w') as file:
            file.write('')
        assert db_path.exists()
        assert not dbf.does_db_exist()
        # remove the file for now
        db_path.unlink()

    def test_create_pos_db(self, db_path):
        assert not db_path.exists()
        dbf.create_pos_db()
        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'SELECT * FROM {dbf.POSITIONS_TABLE_NAME}')
            stuff = c.fetchall()
            c.execute(F"SELECT * FROM {dbf.LANGUAGE_TABLE_NAME}")
            more_stuff = c.fetchall()
        assert stuff is not None
        assert more_stuff is not None

    def test_reset_pos_db(self):
        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'INSERT INTO {dbf.POSITIONS_TABLE_NAME} VALUES (?, ?, ?, ?, ?)', ('abc', 0, 0, 0, '1,2,3'))
            conn.commit()
            c.execute(f'SELECT * FROM {dbf.POSITIONS_TABLE_NAME}')
            stuff = c.fetchall()
        assert stuff
        dbf.reset_pos_db()

        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'SELECT * FROM {dbf.POSITIONS_TABLE_NAME}')
            stuff = c.fetchall()
            c.execute(F"SELECT * FROM {dbf.LANGUAGE_TABLE_NAME}")
            more_stuff = c.fetchall()
        assert not stuff
        assert more_stuff is not None

    def test_save_pos_list_to_db(self, pos_list0):
        dbf.save_pos_list_to_db(pos_list0)

        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'SELECT COUNT(*) FROM {dbf.POSITIONS_TABLE_NAME}')
            assert c.fetchone()[0] > 1
        
    def test_load_pos_list_from_db(self, pos_list0):
        pos_list = dbf.load_pos_list_from_db()

        for pos, pos0 in zip(pos_list, pos_list0):
            assert pos == pos0
            assert pos.pieces == pos0.pieces
            assert pos.stepnum == pos0.stepnum
            assert pos.distance_to_end == pos0.distance_to_end
            assert pos.pos_id == pos0.pos_id
            assert pos.neighbors == pos0.neighbors

    def test_get_pos_by_id(self, pos_list0):
        id_to_test = 0
        pos = dbf.get_pos_by_id(id_to_test)
        assert pos == pos_list0[0]

    def test_get_pos_by_ids(self, pos_list0):
        ids_to_test = {0, 1, 2}
        pos_list = dbf.get_pos_by_ids(ids_to_test)
        for pos, pos0 in zip(pos_list, pos_list0):
            assert pos == pos0
            assert pos.pieces == pos0.pieces
            assert pos.stepnum == pos0.stepnum
            assert pos.distance_to_end == pos0.distance_to_end
            assert pos.pos_id == pos0.pos_id
            assert pos.neighbors == pos0.neighbors


    def test_generate_language_table(self, monkeypatch, languages):
        monkeypatch.setattr(dbf, 'get_languages', lambda *args: languages)
        dbf.generate_language_table()

        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            c.execute(f'SELECT * FROM {dbf.LANGUAGE_TABLE_NAME}')
            language_rows = c.fetchall()
        assert language_rows
        assert [l for l, _, _ in language_rows] == list(languages)
        default_values = [row[1] for row in language_rows]
        assert any(default_values)
        assert not all(default_values)

    def test_get_languages_from_db(self, languages):
        # language_list = dbf.get_languages()
        assert dbf.get_languages_from_db() == list(languages)

    @pytest.mark.parametrize(
        'index', [0, 1]
    )
    def test_set_default_language(self, index, languages):
        dbf.set_default_language(languages[index])

        assert dbf.get_default_language() == languages[index]


    
    @pytest.mark.parametrize(
        ('column_name', 'expected_result'), [
            ('id', (True, None)),
            ('dist_from_end', (False, -1))
        ]
    )
    def test_check_column(self, column_name, expected_result):
        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            assert dbf.check_column(c, column_name) == expected_result

    def test_check_neighbor_column(self):
        with dbf.sqlite3.connect(dbf.DB_FILEPATH) as conn:
            c = conn.cursor()
            assert not dbf.check_neighbor_column(c)
    
    @pytest.mark.parametrize(
        'check_passed', [True, False]
    )
    def test_check_pos_db(self, monkeypatch, check_passed):
        monkeypatch.setattr(dbf, 'check_db_columns', lambda *args: check_passed)
        assert dbf.check_pos_db() == check_passed


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
            ({-1, 52, 156, 13011}, '-1,52,156,13011'),
            (set(), '')
        ]
    )
    def test_change_neighbor_string_to_set(self, int_set, set_str):
        assert dbf.change_neighbor_string_to_set(set_str) == int_set

    @pytest.mark.parametrize(
        'int_set', [
            {1, 2, 3, 4},
            {-1, 52, 156, 13011},
            set()
        ]
    )
    def test_change_int_set_to_string(self, int_set):
        int_set_as_str = dbf.change_int_set_to_string(int_set)
        assert isinstance(int_set_as_str, str)
        # assert dbf.change_int_set_to_string(int_set) == set_str
        assert dbf.change_neighbor_string_to_set(int_set_as_str) == int_set

    @pytest.mark.parametrize(
        ('stepnum', 'dist_to_end', 'pos_id', 'neighbors'), [
            (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000), (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000))),
            (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000), (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000))),
            (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000), (randint(-1, 64000), randint(-1, 64000), randint(-1, 64000)))
        ]
    )
    def test_table_row_to_position(self, stepnum, dist_to_end, pos_id, neighbors):
        pieces_str = '4,8,13,19,0,2,15,17,7,5'
        # stepnum = randint(-1, 64000)
        # dist_to_end = randint(-1, 64000)
        # pos_id = randint(-1, 64000)
        # neighbor_str = '-1,52,156,13011'
        neighbor_str = dbf.change_int_set_to_string(neighbors)
        row = (pieces_str, stepnum, dist_to_end, pos_id, neighbor_str)
        pos = dbf.table_row_to_position(row)
        assert pos.pieces == dbf.Positions().pieces
        assert pos.stepnum == stepnum
        assert pos.distance_to_end == dist_to_end
        assert pos.pos_id == pos_id
        assert pos.neighbors == set(neighbors)

    def test_position_to_table_row(self):
        pos = dbf.Positions()
        expected_row = ('4,8,13,19,0,2,15,17,7,5', 0, -1, 0, '')
        assert dbf.position_to_table_row(pos) == expected_row

