import tkinter as tk
import zipfile

from menu_commands import COMMANDS
from ui_components.menu_bar import create_menu
from ui_components.file_explorer import FileExplorer
from ui_components.limits_display import TableDisplay

class TestEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Informejtycy Test Editor")
        self.geometry("800x600")

        # Create menu
        create_menu(self, COMMANDS)
        self.bind_shortcuts()

        # Create UI layout
        self.table: TableDisplay | None = None
        self.file_explorer: FileExplorer | None = None
        self.right_frame = None
        self.main_display = None
        self.create_widgets()

        self.changes_buffer = {}
        self.current_test = None

        self.file_explorer.load_pack('tests/suma-n-liczb.test')
        limits = self.file_explorer.load_config('tests/suma-n-liczb.test')
        self.table.update_limits(limits[0], limits[1])

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Right side container
        self.right_frame = tk.Frame(self, bd=2, relief="sunken")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid_rowconfigure(0, weight=0)  # Table stays its natural height
        self.right_frame.grid_rowconfigure(1, weight=1)  # Allow main_display to expand
        self.right_frame.grid_columnconfigure(0, weight=1)  # Make both table & content expand horizontally

        # Placeholder for main content
        self.main_display = tk.Frame(self.right_frame, bg="white", bd=2, relief="solid", height=300)
        self.main_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid_rowconfigure(1, weight=1)

        # File Explorer on the left
        self.file_explorer = FileExplorer(self, self.display_test, self.hide_tests)
        self.file_explorer.grid(row=0, column=0, sticky="ns")

        # Table for time/memory limits
        self.table = TableDisplay(self.right_frame)
        self.table.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def display_test(self, test_name):
        """Displays the content of inX and outX in text areas."""
        test_number = test_name[4:]  # Extract number from testX
        in_file = f"in{test_number}"
        out_file = f"out{test_number}"
        self.current_test = test_name

        # Destroy the existing main_display and create a new one
        self.hide_tests()

        input_label = tk.Label(self.main_display, text="Input", font=("Arial", 10, "bold"))
        input_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        output_label = tk.Label(self.main_display, text="Output", font=("Arial", 10, "bold"))
        output_label.grid(row=2, column=0, sticky="w", padx=5, pady=(5, 0))

        # Scrollbars
        input_scroll = tk.Scrollbar(self.main_display, orient="vertical")
        output_scroll = tk.Scrollbar(self.main_display, orient="vertical")

        # Create text areas
        self.input_text = tk.Text(
            self.main_display, height=10, wrap="word",
            yscrollcommand=input_scroll.set
        )
        self.output_text = tk.Text(
            self.main_display, height=10, wrap="word",
            yscrollcommand=output_scroll.set
        )

        input_scroll.config(command=self.input_text.yview)
        output_scroll.config(command=self.output_text.yview)

        # Load from buffer if exists, otherwise read from ZIP
        if test_name in self.changes_buffer:
            self.input_text.insert(tk.INSERT, self.changes_buffer[test_name]["input"])
            self.output_text.insert(tk.INSERT, self.changes_buffer[test_name]["output"])
        elif hasattr(self.file_explorer, "current_pack"):
            with zipfile.ZipFile(self.file_explorer.current_pack, 'r') as zip_ref:
                self.input_text.insert(tk.INSERT, zip_ref.read(in_file).decode('utf-8'))
                self.output_text.insert(tk.INSERT, zip_ref.read(out_file).decode('utf-8'))

        def _on_mouse_wheel(event, widget):
            widget.yview_scroll(-1 * (event.delta // 120), "units")

        self.input_text.bind("<MouseWheel>", lambda e: _on_mouse_wheel(e, self.input_text))
        self.output_text.bind("<MouseWheel>", lambda e: _on_mouse_wheel(e, self.output_text))

        self.input_text.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)
        input_scroll.grid(row=1, column=1, sticky="ns", padx=(0, 5))

        self.output_text.grid(row=3, column=0, sticky="nsew", padx=(5, 0), pady=5)
        output_scroll.grid(row=3, column=1, sticky="ns", padx=(0, 5))

        self.input_text.bind("<KeyRelease>", lambda e: self.save_to_buffer())
        self.output_text.bind("<KeyRelease>", lambda e: self.save_to_buffer())

        # Pack text areas
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.output_text.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        self.main_display.grid_rowconfigure(1, weight=1)  # Input text expands
        self.main_display.grid_rowconfigure(3, weight=1)  # Output text expands
        self.main_display.grid_columnconfigure(0, weight=1)  # Full width

    def hide_tests(self):
        self.main_display.destroy()
        self.main_display = tk.Frame(self.right_frame, bg="white", bd=2, relief="solid")
        self.main_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)


    def save_to_buffer(self):
        """Saves changes to buffer."""
        if self.current_test:
            self.changes_buffer[self.current_test] = {
                "input": self.input_text.get("1.0", tk.END).strip(),
                "output": self.output_text.get("1.0", tk.END).strip()
            }

    def bind_shortcuts(self):
        """Bind shortcuts."""
        self.bind_all("<Control-Shift-N>", lambda e: COMMANDS["new"](self))
        self.bind_all("<Control-o>", lambda e: COMMANDS["open"](self))
        self.bind_all("<Control-s>", lambda e: COMMANDS["save"](self))

        self.bind_all("<Control-n>", lambda e: COMMANDS["new_test"](self))
        self.bind_all("<Delete>", lambda e: COMMANDS["delete_test"](self))
        self.bind_all("<Control-l>", lambda e: COMMANDS["limits"](self))
        self.bind_all("<Control-Shift-V>", lambda e: COMMANDS["validate"](self))

if __name__ == "__main__":
    app = TestEditorApp()
    app.mainloop()
