import os
import re
import zipfile
import tkinter as tk
from tkinter import ttk

from exceptions import WrongConfigException, ConfigNotFound

class FileExplorer(tk.Frame):
    def __init__(self, parent, on_file_selected, on_file_unselected):
        super().__init__(parent, bd=2, relief="sunken")
        self.pack_propagate(False)
        self.config(width=200)

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)

        self.root_node = self.tree.insert("", "end", text="", open=True)
        self.tree.tag_configure("bold", font=("Arial", 10, "bold"))
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        self.on_file_selected = on_file_selected
        self.on_file_unselected = on_file_unselected
        self.current_pack = None

    def load_pack(self, file_path):
        """Loads ZIP file and displays the structured file hierarchy"""
        self.current_pack = file_path

        self.tree.delete(*self.tree.get_children())  # Clear previous entries
        self.root_node = self.tree.insert("", "end", text=os.path.basename(file_path).split('.')[0], open=True, tags=("bold",))

        with zipfile.ZipFile(file_path, 'r') as pack_file:
            file_structure = sorted(pack_file.namelist())

        test_cases = {}  # Dictionary to store test cases as {X: "testX"}

        for file in file_structure:
            if file == "CONFIG":
                continue  # Skip CONFIG file

            match_in = re.match(r"in(\d+)$", file)
            match_out = re.match(r"out(\d+)$", file)

            if match_in:
                test_cases[match_in.group(1)] = f"test{match_in.group(1)}"
            elif match_out:
                test_cases[match_out.group(1)] = f"test{match_out.group(1)}"

        # Add test cases to the treeview
        for X in sorted(test_cases.keys(), key=int):
            self.tree.insert(self.root_node, "end", text=test_cases[X])

    def load_config(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as pack_file:
            try:
                limits = pack_file.read('CONFIG').decode('utf-8')
            except FileNotFoundError:
                raise ConfigNotFound("Config file not found in the pack")

            if len(limits.split(' ')) == 2:
                limits = limits.split(' ')
            elif len(limits.split('\r\n')) == 2:
                limits = limits.split('\r\n')
            elif len(limits.split('\n')) == 2:
                limits = limits.split('\n')
            else:
                raise WrongConfigException("Config file format is incorrect")

            return limits[0], limits[1]

    def on_item_selected(self, event):
        """Handles when a file is selected in the treeview."""
        selected_item = self.tree.selection()
        if selected_item:
            file_name = self.tree.item(selected_item[0], "text")
            if file_name.startswith("test"):
                self.on_file_selected(file_name)  # Call main app function
            else:
                self.on_file_unselected()
