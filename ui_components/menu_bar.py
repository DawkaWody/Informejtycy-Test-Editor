import tkinter as tk
from typing import Callable
from functools import partial

def create_menu(root, commands: dict[str, Callable]):
    menubar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New pack   Ctrl+Shift+N", command=partial(commands["new"], root))
    file_menu.add_command(label="Open existing  Ctrl+O", command=partial(commands["open"], root))
    file_menu.add_command(label="Save   Ctrl+S", command=partial(commands["save"], root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Pack Menu
    pack_menu = tk.Menu(menubar, tearoff=0)
    pack_menu.add_command(label="New test   Ctrl+N", command=partial(commands["new_test"], root))
    pack_menu.add_command(label="Delete selected test   Del", command=partial(commands["delete_test"], root))
    pack_menu.add_command(label="Configure limits   Ctrl+L", command=partial(commands["limits"], root))
    pack_menu.add_command(label="Validate   Ctrl+Shift+V", command=partial(commands["validate"], root))
    menubar.add_cascade(label="Pack", menu=pack_menu)

    # Options Menu
    options_menu = tk.Menu(menubar, tearoff=0)
    options_menu.add_command(label="Open test directory", command=partial(commands["open_dir"], root))
    options_menu.add_command(label="Force validator re-clone", command=partial(commands["remove_pack_loader"], root))
    options_menu.add_command(label="Open log", command=partial(commands["open_log"], root))
    menubar.add_cascade(label="Options", menu=options_menu)

    # About Menu
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="Version", command=partial(commands["version"], root))
    about_menu.add_command(label="GitHub", command=partial(commands["github"], root))
    about_menu.add_command(label="Bug Report", command=partial(commands["bugreport"], root))
    menubar.add_cascade(label="About", menu=about_menu)

    root.config(menu=menubar)
