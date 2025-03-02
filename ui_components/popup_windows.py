import tkinter as tk

class InputPopup(tk.Toplevel):
    def __init__(self, parent, title="Enter Values"):
        super().__init__(parent)
        self.title(title)
        self.geometry("270x120")

        self.result = ()  # Stores input values

        # Labels
        tk.Label(self, text="Time limit (sec):").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Memory limit (mb):").grid(row=1, column=0, padx=5, pady=5)

        # Entry fields
        self.entry1 = tk.Entry(self)
        self.entry2 = tk.Entry(self)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self, text="OK", command=self.on_ok).grid(row=2, column=0, columnspan=2, pady=10)

        self.transient(parent)  # Make popup modal
        self.grab_set()  # Disable interactions with main window until closed
        self.wait_window()  # Wait for popup to close

    def on_ok(self):
        """Retrieve values and close the popup."""
        self.result = (self.entry1.get(), self.entry2.get())
        self.destroy()

class LoadingPopup(tk.Toplevel):
    def __init__(self, parent, message, title="Loading..."):
        super().__init__(parent)
        self.title(title)
        self.geometry("270x120")
        self.resizable(False, False)

        tk.Label(self, text=message, font=("Arial", 12)).pack(pady=20)

        self.transient()
        self.grab_set()
