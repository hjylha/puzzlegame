from pathlib import Path
import sqlite3
from positions import Positions
from puzzlegame_setup import NUM_OF_ROWS, get_languages, get_texts_in_language

DB_FILENAME = "position.db"
DB_FILEPATH = Path(__file__).parent / DB_FILENAME

POSITIONS_TABLE_NAME = "positions"
LANGUAGE_TABLE_NAME = "languages"


# first some functions to change data to suitable form
# 
# transforming (x, y) coordinates to single number (and back)
def coord_as_int(coord):
    return coord[0] + coord[1] * NUM_OF_ROWS

def int_as_coord(num):
    return (num % NUM_OF_ROWS, num // NUM_OF_ROWS)


# transforming tuple of coords to a string of ints (and vice versa)
def change_pos_tuple_to_string(pos_tuple):
    int_coords = [coord_as_int(coord) for coord in pos_tuple]
    return ",".join([str(num) for num in int_coords])

def change_pos_string_to_tuple(pos_as_string):
    int_coords = pos_as_string.split(",")
    return tuple(int_as_coord(int(num)) for num in int_coords)


# transforming a set of ints to a string of ints (and vice versa)
def change_int_set_to_string(int_set):
    if int_set == set():
        return ''
    return ",".join([str(num) for num in int_set])

def change_neighbor_string_to_set(set_as_string):
    if set_as_string == '':
        return set()
    return set(int(num) for num in set_as_string.split(","))
    

# construct a Positions object based on a row in positions table
def table_row_to_position(table_row):
    pos_coords = change_pos_string_to_tuple(table_row[0])
    neighbors = change_neighbor_string_to_set(table_row[4])
    return Positions(pos_coords, table_row[1], table_row[2], table_row[3], neighbors)

def position_to_table_row(pos):
    pieces_str = change_pos_tuple_to_string(pos.pieces)
    neighbors = change_int_set_to_string(pos.neighbors)
    return (pieces_str, pos.stepnum, pos.distance_to_end, pos.pos_id, neighbors)


# now onto the actual db operations
# 
def perform_db_actions(function_to_execute, *args):
    with sqlite3.connect(DB_FILEPATH) as conn:
        to_return = function_to_execute(conn, *args)
    return to_return


def execute_commands(conn, *commands):
    c = conn.cursor()
    for command in commands:
        c.execute(command)
        conn.commit()
    return


# try to select stuff
def try_select(conn):
    c = conn.cursor()
    command = f"SELECT * FROM {POSITIONS_TABLE_NAME}"
    try:
        c.execute(command)
        return True
    except sqlite3.OperationalError:
        return False


# return all the rows with ids in a given list
def select_pos_by_id(conn, pos_id_list):
    condition = " OR ".join(["id = ?" for _ in pos_id_list])
    command = f"SELECT * FROM {POSITIONS_TABLE_NAME} WHERE {condition}"
    c = conn.cursor()
    c.execute(command, pos_id_list)
    return c.fetchall()


def perform_db_commands(command_to_execute, *args):
    perform_db_actions(execute_commands, command_to_execute, *args)
    # with sqlite3.connect(DB_FILEPATH) as conn:
    #     c = conn.cursor()
    #     c.execute(command_to_execute)
    #     # maybe there are more commands
    #     if args:
    #         conn.commit()
    #         for command in args:
    #             c.execute(command)
    #             conn.commit()


def create_pos_db_command():
    return f"""CREATE TABLE {POSITIONS_TABLE_NAME} (
        position TEXT UNIQUE NOT NULL,
        dist_from_start INTEGER,
        dist_from_end INTEGER,
        id INTEGER UNIQUE NOT NULL,
        neighbors TEXT
    )
        """

def create_language_table_command():
    return f"""CREATE TABLE {LANGUAGE_TABLE_NAME} (
        abbreviation TEXT UNIQUE NOT NULL,
        default_language INTEGER NOT NULL,
        description TEXT )"""


# Is this a good way to structure the database???
def create_pos_db():
    perform_db_commands(create_pos_db_command(), create_language_table_command())
    print(f"Database '{DB_FILENAME}' created")


def reset_pos_db():
    perform_db_commands(f"DROP TABLE {POSITIONS_TABLE_NAME}", 
                        f"DROP TABLE {LANGUAGE_TABLE_NAME}", 
                        create_pos_db_command(),
                        create_language_table_command())
    print(f"Database '{DB_FILENAME}' reset")


def does_db_exist():
    if not DB_FILEPATH.exists():
        return False
    return perform_db_actions(try_select)


def check_column(cursor, column_name):
    cursor.execute(f"SELECT COUNT(*) FROM {POSITIONS_TABLE_NAME} WHERE {column_name} < ?", (0, ))
    bad_count = cursor.fetchone()[0]
    if bad_count:
        return (False, -1)
    cursor.execute(f"SELECT MAX({column_name}) FROM {POSITIONS_TABLE_NAME}")
    max_column_value = cursor.fetchone()[0]
    for value in range(max_column_value + 1):
        cursor.execute(f"SELECT COUNT(*) FROM {POSITIONS_TABLE_NAME} WHERE {column_name} = ?", (value,))
        count = cursor.fetchone()[0]
        if count == 0:
            return (False, value)
    return (True, None)

# neighbor column should not have empty strings
def check_neighbor_column(cursor):
    cursor.execute(f"SELECT * FROM {POSITIONS_TABLE_NAME} WHERE neighbors = ?", ("",))
    if cursor.fetchall():
        return False
    return True

def check_pos_columns(conn):
    c = conn.cursor()
    if not check_neighbor_column(c):
        print("ERROR: Empty strings in neighbors column.")
        return False
    for name in ("dist_from_end", "dist_from_start", "id"):
        is_ok, value = check_column(c, name)
        if not is_ok:
            if value == -1:
                print(f"ERROR: Unassigned values in column {name}")
            else:
                print(f"ERROR: No rows with value {value} in column {name}")
            return False
    return True

def check_language_table(conn):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {LANGUAGE_TABLE_NAME}")
    language_rows = c.fetchall()
    if not language_rows:
        print("ERROR: No languages saved to database.")
        return False
    for language in [l for l, _, _ in language_rows]:
        if not get_texts_in_language(language):
            return False
    return any([default_l for _, default_l, _ in language_rows])

def check_pos_db():
    # check languages
    if not perform_db_actions(check_language_table):
        return False
    # check columns
    if not perform_db_actions(check_pos_columns):
        return False
    # check that initial position is in db
    pos = get_pos_by_id(0)
    if not pos:
        return False
    return pos == Positions()


# moving on to inserting positions to db
def insert_positions(conn, pos_list):
    c = conn.cursor()
    for pos in pos_list:
        c.execute(f"INSERT INTO {POSITIONS_TABLE_NAME} VALUES (?, ?, ?, ?, ?)", position_to_table_row(pos))

    
def save_pos_list_to_db(pos_list):
    perform_db_actions(insert_positions, pos_list)


# getting all positions from db
def select_all_positions(conn):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {POSITIONS_TABLE_NAME}")
    pos_list_raw = c.fetchall()
    return [table_row_to_position(row) for row in pos_list_raw]

def load_pos_list_from_db():
    return perform_db_actions(select_all_positions)


# and then getting positions with given ids
def get_pos_by_id(pos_id):
    # command = f"SELECT * FROM {POSITIONS_TABLE_NAME} WHERE id = ?"
    data_row = perform_db_actions(select_pos_by_id, [pos_id])[0]
    return table_row_to_position(data_row)
    

def get_pos_by_ids(pos_ids):
    # command = f"SELECT * FROM {POSITIONS_TABLE_NAME} WHERE id = ?"
    data_rows = perform_db_actions(select_pos_by_id, list(pos_ids))
    return [table_row_to_position(row) for row in data_rows]


def save_languages_to_db(conn, language_list):
    cursor = conn.cursor()
    for i, language in enumerate(language_list):
        row = (language, False if i != 0 else True, "")
        cursor.execute(f"INSERT INTO {LANGUAGE_TABLE_NAME} VALUES ( ?, ?, ? )", row)
        # conn.commit()


def set_default_language_action(conn, new_default_language):
    cursor = conn.cursor()
    command = f"SELECT rowid FROM {LANGUAGE_TABLE_NAME} WHERE default_language= ?"
    cursor.execute(command, (True, ))
    if rowid := cursor.fetchone()[0]:
        command = f"UPDATE {LANGUAGE_TABLE_NAME} SET default_language= ? WHERE rowid = ?"
        cursor.execute(command, (False, rowid))
    command = f"UPDATE {LANGUAGE_TABLE_NAME} SET default_language= ? WHERE abbreviation = ?"
    cursor.execute(command, (True, new_default_language))


def get_default_language_action(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT abbreviation FROM {LANGUAGE_TABLE_NAME} WHERE default_language= ?", (True,))
    return cursor.fetchone()[0]


def generate_language_table():
    languages = get_languages()
    perform_db_actions(save_languages_to_db, languages)


def get_languages_from_db():
    
    def select_languages(conn):
        c = conn.cursor()
        command = f"SELECT abbreviation FROM {LANGUAGE_TABLE_NAME}"
        c.execute(command)
        return c.fetchall()
    
    language_rows = perform_db_actions(select_languages)
    return [row[0] for row in language_rows]


def set_default_language(new_default_language):
    perform_db_actions(set_default_language_action, new_default_language)

def get_default_language():
    return perform_db_actions(get_default_language_action)


def find_solution_from_db(conn, start_pos):
    # start_pos = get_pos_by_id(start_pos_id)
    pos_list = [start_pos]
    c = conn.cursor()
    while pos_list[-1].distance_to_end > 0:
        ids = ", ".join(["?" for _ in pos_list[-1].neighbors])
        command = f"SELECT * FROM {POSITIONS_TABLE_NAME} WHERE id IN ( {ids} ) AND dist_from_end < ?"
        c.execute(command, list(pos_list[-1].neighbors) + [pos_list[-1].distance_to_end])
        row = c.fetchone()
        if row:
            pos_list.append(table_row_to_position(row))
    return pos_list

def find_opt_solution(start_pos_id):
    start_pos = get_pos_by_id(start_pos_id)
    return perform_db_actions(find_solution_from_db, start_pos)
