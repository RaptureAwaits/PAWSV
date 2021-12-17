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

    def rows_to_dict(self, row_list):
        row_dicts = []
        for row in row_list:
            row_dict = {}
            row_dict['title'] = row[0]
            row_dict['artist'] = row[1]
            row_dict['path'] = row[2]
            row_dicts.append(row_dict)
        return row_dicts

    def row_dict_to_string(self, row_dict):
        return f"{row_dict['artist']} -- {row_dict['title']} -- {row_dict['path']}"

    def string_to_row_dict(self, entry_string):
        row_dict = {}
        fields = entry_string.split(" -- ")
        row_dict['artist'] = fields[0]
        row_dict['title'] = fields[1]
        row_dict['path'] = fields[2]
        return row_dict

    def get_all_rows(self):
        self.c.execute('SELECT * FROM tunes')
        rows = self.c.fetchall()
        return rows

    def add_row(self, title, artist, path):
        self.c.execute('INSERT INTO tunes VALUES (?, ?, ?)', (title, artist, path))
        self.commit()
        return f"Added '{title}' by '{artist}' to the database"

    def delete_row(self, title, artist, path):
        self.c.execute('DELETE FROM tunes WHERE path=(?)', (path,))
        self.commit()
        return f"Removed '{title}' by '{artist}' from the database"
