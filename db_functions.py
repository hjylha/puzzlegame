from pathlib import Path
import sqlite3
from positions import Positions
from puzzlegame_setup import NUM_OF_ROWS

DB_FILENAME = "position.db"
DB_FILEPATH = Path(__file__).parent / DB_FILENAME

POSITIONS_TABLE_NAME = "positions"


def perform_db_actions(command_to_execute, *args):
    with sqlite3.connect(DB_FILEPATH) as conn:
        c = conn.cursor()
        c.execute(command_to_execute)
        # maybe there are more commands
        if args:
            conn.commit()
            for command in args:
                c.execute(command)
                conn.commit()


def create_pos_db_command():
    return f"""CREATE TABLE {POSITIONS_TABLE_NAME} (
        position TEXT,
        dist_from_start INTEGER,
        dist_from_end INTEGER,
        id INTEGER,
        neighbors TEXT
    )
        """

# Is this a good way to structure the database???
def create_pos_db():
    perform_db_actions(create_pos_db_command())
    # conn = sqlite3.connect(DB_FILEPATH)
    # c = conn.cursor()
    # c.execute("""CREATE TABLE positions (
    #     position TEXT,
    #     dist_from_start INTEGER,
    #     dist_from_end INTEGER,
    #     id INTEGER,
    #     neigbors TEXT
    # )
    #     """)
    # conn.commit()
    # conn.close()
    print(f"Database '{DB_FILENAME}' created")

def reset_pos_db():
    perform_db_actions(f"DROP TABLE {POSITIONS_TABLE_NAME}", create_pos_db_command())
    # conn = sqlite3.connect(DB_FILEPATH)
    # c = conn.cursor()

    # c.execute("DROP TABLE positions")
    # conn.commit()

    # c.execute("""CREATE TABLE positions (
    #     position TEXT,
    #     dist_from_start INTEGER,
    #     dist_from_end INTEGER,
    #     id INTEGER,
    #     neigbors TEXT
    # )
    #     """)
    # conn.commit()
    # conn.close()
    print(f"Database '{DB_FILENAME}' reset")

def does_db_exist():
    if not DB_FILEPATH.exists():
        return False
    conn = sqlite3.connect("position.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM positions")
        return True
    except sqlite3.OperationalError:
        return False

def check_pos_db():
    conn = sqlite3.connect("position.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM positions WHERE dist_from_end > -1")
        test_list = c.fetchall()
        test_list0 = [item for item in test_list if item[2] == 0]
        if len(test_list) == 13011:
            if len(test_list0) == 484:
                conn.close()
                return True
            else:
                conn.close()
                print("number of end positions in the database is not correct")
                return False
        elif len(test_list) > 0:
            print(len(test_list))
            print("Database has something, but also problems")
        conn.close()
        return False
    except sqlite3.OperationalError:
        conn.close()
        return False


def save_pos_list_to_db(pos_list):
    conn = sqlite3.connect("position.db")
    c = conn.cursor()
    for pos in pos_list:
        pieces = change_pos_tuple_to_string(pos.pieces)
        neighbors = change_int_set_to_string(pos.neighbors)
        # maybe distance_to_end has not been calculated yet
        c.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?)", (pieces, pos.stepnum, pos.distance_to_end, pos.pos_id, neighbors))
    conn.commit()
    conn.close()

def load_pos_list_from_db():
    conn = sqlite3.connect("position.db")
    c = conn.cursor()
    c.execute("SELECT * FROM positions")
    pos_list_raw = c.fetchall()
    conn.close()
    # format the pos list
    pos_list = []
    for item in pos_list_raw:
        pos_coords = change_pos_string_to_tuple(item[0])
        neighbors = change_neighbor_string_to_set(item[4])
        pos = Positions(pos_coords, item[1], item[2], item[3], neighbors)
        # pos.pos_id = item[3]
        
        pos_list.append(pos)
    return pos_list


def coord_as_int(coord):
    return coord[0] + coord[1] * NUM_OF_ROWS

def int_as_coord(num):
    return (num % NUM_OF_ROWS, num // NUM_OF_ROWS)


def change_pos_tuple_to_string(pos_tuple):
    int_coords = [coord_as_int(coord) for coord in pos_tuple]
    return ",".join([str(num) for num in int_coords])


# how to get info from position string to position tuple
def change_pos_string_to_tuple(pos_as_string):
    int_coords = pos_as_string.split(",")
    return tuple(int_as_coord(int(num)) for num in int_coords)


def change_int_set_to_string(int_set):
    return ",".join([str(num) for num in int_set])


def change_neighbor_string_to_set(set_as_string):
    return set(int(num) for num in set_as_string.split(","))
    