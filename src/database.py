import sqlite3
import os

db_path = "../resource/tunes.db"


class db:
    def load_table(self):
        if not os.path.isfile(db_path):  # Establishes a new database if needed
            print("No file at resource/tunes.db cannot be found, creating new file...")
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('CREATE TABLE tunes (title TEXT, artist TEXT, path TEXT)')
            conn.commit()
        else:
            print("Located resource/tunes.db...")
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
        return c, conn

    def __init__(self):
        self.c, self.conn = self.load_table()

    def commit(self):
        self.conn.commit()

    def add_row(self, title, artist, path):
        self.c.execute('INSERT INTO tunes VALUES (?, ?, ?)', (title, artist, path))
        self.commit()
        print(f"Added '{title}' by '{artist}' to the database")