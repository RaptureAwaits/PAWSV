import tkinter as tk
import tkinter.filedialog

from database import db as db_connection


class FileManager:  # Dialog for adding audio files to the database
    def __init__(self, parent):
        self.win = tk.Tk()
        self.parent = parent
        self.db = parent.db
        self.win.title("PAWS-V File Manager")

        # Browse File button that opens Windows file dialog
        self.fd_button = tk.Button(self.win, text="Browse Files", command=self.open_fd)
        self.fd_button.grid(column=0, row=0)

        # The text field that will display the file path after a file is selected
        self.path_display = tk.Entry(self.win, width=50)
        self.path_display.grid(column=1, row=0)

        # Label and text field for the user to specify audio title
        self.title_label = tk.Label(self.win, text="Title:")
        self.title_label.grid(column=0, row=1)
        self.title_field = tk.Entry(self.win, width=50)
        self.title_field.grid(column=1, row=1)

        # Label and text field for the user to specify audio artist
        self.title_label = tk.Label(self.win, text="Artist:")
        self.title_label.grid(column=0, row=2)
        self.artist_field = tk.Entry(self.win, width=50)
        self.artist_field.grid(column=1, row=2)

        # Add to database button
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

        if "--" in title or "--" in artist or "--" in path:
            self.parent.log("Audio not added: Text fields cannot contain the string '--'...\n")
            self.win.destroy()
            return

        self.db.add_row(title, artist, path)
        self.parent.populate_select_box()
        self.parent.log(f"Added {title} by {artist} to the database.\n")
        self.win.destroy()


class UserInterface:  # Main UI that will branch to all other UI components
    def __init__(self):
        self.win = tk.Tk()
        self.db = db_connection()
        self.win.title("PAWS-V Interface")

        # Add file button: creates a file dialog object
        self.add_file_button = tk.Button(self.win, text="Add File", command=self.open_fm)
        self.add_file_button.grid(column=0, row=0)

        # Delete file button: calls the delete file method
        self.rm_file_button = tk.Button(self.win, text="Remove File", command=self.rm_entry)
        self.rm_file_button.grid(column=0, row=1)

        # Play file button: plays the selected audio file
        self.play_file_button = tk.Button(self.win, text="Play Audio")
        self.play_file_button.grid(column=0, row=2)

        # The selection box for audio tracks in the database
        self.audio_select = tk.Listbox(self.win, width=100, selectmode=tk.SINGLE)
        self.audio_select.grid(column=1, row=0, rowspan=3, sticky=tk.N + tk.S)

        # The text box that displays program logs
        self.log_display = tk.Text(self.win, height=3, width=20)
        self.log_display.grid(column=0, row=3, columnspan=2, sticky=tk.W + tk.E)

        self.populate_select_box()
        self.win.mainloop()

    def open_fm(self):
        fm = FileManager(self)
        self.populate_select_box()

    def rm_entry(self):
        selection = self.audio_select.curselection()
        if not selection:
            self.log("Please select a track to remove first...\n")
            return
        entry = self.audio_select.get(selection[0])
        entry_dict = self.db.string_to_row_dict(entry)
        self.db.delete_row(entry_dict['title'], entry_dict['artist'], entry_dict['path'])
        self.log(f"Removed {entry_dict['title']} by {entry_dict['artist']} from the database.\n")
        self.populate_select_box()

    def log(self, log_text):
        self.log_display.insert(tk.END, log_text)
        self.log_display.see(tk.END)

    def populate_select_box(self):
        rows = self.db.get_all_rows()
        row_dicts = self.db.rows_to_dict(rows)

        select_box_size = self.audio_select.size()
        self.audio_select.delete(0, select_box_size)

        sorted_row_dicts = sorted(row_dicts, key=lambda rd: rd['artist'])
        for row_dict in row_dicts:
            self.audio_select.insert(tk.END, self.db.row_dict_to_string(row_dict))
