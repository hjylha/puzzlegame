# import sqlite3
from positions import Positions

# conn = sqlite3.connect("position.db")
# c = conn.cursor()

# conn.close()

import db_functions as db

# db.save_pos_list_to_db([Positions()])

pos_list = db.load_pos_list_from_db()

print(len(pos_list))

# i = 0
# some_pos = [pos for pos in pos_list if pos.distance_to_end == i]
# while not(some_pos == []):
#     print(i, len(some_pos))
#     i += 1
#     some_pos = [pos for pos in pos_list if pos.distance_to_end == i]


end_pos = [pos for pos in pos_list if pos.distance_to_end == 0]
some_pos = [pos for pos in pos_list if pos.distance_to_end > 0]
bad_pos = [pos for pos in pos_list if pos.distance_to_end < 0]

print(len(bad_pos), "bad positions")

problematic_pos = [pos for pos in some_pos if pos.solved()]
print(len(problematic_pos), "solved pos not marked as solved")

problematic_pos2 = [pos for pos in end_pos if not(pos.solved())]
print(len(problematic_pos2), "not solved positions marked as solved")

print("Database check:")
print("Database OK?", db.check_pos_db())
