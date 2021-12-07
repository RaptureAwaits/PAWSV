import tkinter as tk
import tkinter.filedialog

from database import db


class file_manager:
    def __init__(self):
        self.db = db()
        self.win = tk.Tk()
        self.win.title("PAWS-V File Manager")

        self.fd_button = tk.Button(self.win, text="Browse Files", command=self.open_fd)
        self.fd_button.grid(column=0, row=0)

        self.path_display = tk.Entry(self.win, width=50)
        self.path_display.grid(column=1, row=0)

        self.title_label = tk.Label(self.win, text="Title:")
        self.title_label.grid(column=0, row=1)
        self.title_field = tk.Entry(self.win, width=50)
        self.title_field.grid(column=1, row=1)

        self.title_label = tk.Label(self.win, text="Artist:")
        self.title_label.grid(column=0, row=2)
        self.artist_field = tk.Entry(self.win, width=50)
        self.artist_field.grid(column=1, row=2)

        self.db_button = tk.Button(self.win, text="Add to database", command=self.add_tune)
        self.db_button.grid(column=1, row=3)

        self.win.mainloop()


    def open_fd(self):
        path = tk.filedialog.askopenfilename()
        self.path_display.insert(tk.END, path)

    def add_tune(self):
        title = self.title_field.get()
        artist = self.artist_field.get()
        path = self.path_display.get()

        self.db.add_row(title, artist, path)
        self.win.destroy()


class user_interface:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("PAWS-V Interface")

        self.add_file_button = tk.Button(self.win, text="Add File", command=self.open_fm)
        self.add_file_button.grid(column=0, row=0)

        self.win.mainloop()

    def open_fm(self):
        fm = file_manager()
        print("CONCLUDED")