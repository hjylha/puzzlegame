import db_functions as dbf
import generate_db
import pg_tkinter


if __name__ == "__main__":
    if dbf.does_db_exist() and dbf.check_pos_db():
        pg_tkinter.play_puzzlegame()
    else:
        print("Generating Database. This may take a few minutes.")
        generate_db.generate_db()
        if dbf.does_db_exist() and dbf.check_pos_db():
            pg_tkinter.play_puzzlegame()
    # pg_tkinter.play_puzzlegame()
