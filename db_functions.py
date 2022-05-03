import sqlite3
from positions import Positions
from puzzlegame_setup import piece_num

# Is this a good way to structure the database???
def create_pos_db():
    conn = sqlite3.connect("position.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE positions (
        position TEXT,
        dist_from_start INTEGER,
        dist_from_end INTEGER,
        id INTEGER,
        neigbors TEXT
    )
        """)
    conn.commit()
    conn.close()
    print("Database 'position.db' created")

def reset_pos_db():
    conn = sqlite3.connect("position.db")
    c = conn.cursor()

    c.execute("DROP TABLE positions")
    conn.commit()

    c.execute("""CREATE TABLE positions (
        position TEXT,
        dist_from_start INTEGER,
        dist_from_end INTEGER,
        id INTEGER,
        neigbors TEXT
    )
        """)
    conn.commit()
    conn.close()
    print("Database 'position.db' reset")

def does_db_exist():
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
        # maybe distance_to_end has not been calculated yet
        c.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?)", (str(pos.pieces), pos.stepnum, pos.distance_to_end, pos.pos_id, str(pos.neighbors)))
        # this does not work
        # c.execute(f"INSERT INTO positions VALUES ({str(pos.pieces)}, {pos.stepnum}, {pos.distance_to_end})")
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
        pos = Positions(pos_coords, item[1], item[2])
        pos.pos_id = item[3]
        pos.neighbors = change_neighbor_string_to_set(item[4])
        pos_list.append(pos)
    return pos_list


# how to get info from position string to position tuple
def change_pos_string_to_tuple(pos_as_string):
    chars = "01234"

    # def is_char_in_chars(a):
    #     if a in chars:
    #         return True
    #     else:
    #         return False

    # initial_list = pos_as_string.split(", ")
    initial_list = list(pos_as_string)
    # list_of_coords = list(filter(is_char_in_chars, initial_list))
    list_of_coords = list(filter(lambda c: c in chars, initial_list))
    pos_list = []
    for i in range(piece_num):
        pos_list.append((int(list_of_coords[2 * i]), int(list_of_coords[2 * i + 1])))
    return tuple(pos_list)

def change_neighbor_string_to_set(set_as_string):
    neighbor_set = set()
    chars = "0123456789"
    str_num = ""
    found_number = False
    for char in set_as_string:
        if char in chars:
            found_number = True
            str_num = str_num + char
        else:
            if found_number:
                neighbor_set.add(int(str_num))
                str_num = ""
            found_number = False
    return neighbor_set
    