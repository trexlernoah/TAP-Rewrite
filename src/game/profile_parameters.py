import tkinter as tk
from tksheet import Sheet


class ProfileParameters(tk.Toplevel):
    def __init__(self, master, rows: int):
        self.rows = rows
        tk.Toplevel.__init__(self, master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.sheet = Sheet(
            self.frame,
            data=[["", "", ""] for r in range(rows)],
            theme="light blue",
            height=520,
            width=480,
        )

        self.sheet.enable_bindings("single_select", "undo", "arrowkeys", "move_columns")
        # self.sheet.set_options(auto_resize_rows=20)
        self.sheet.headers(["Win or Lose", "Shock", "Feedback"])

        self.sheet.dropdown(
            "A",
            values=["Win", "Lose"],
            set_value="",
            selection_function=self.enable_dropdowns,
        )
        self.sheet.dropdown("B", values=list(range(1, 11)), set_value="")
        self.sheet.dropdown("C", values=list(range(1, 11)), set_value="")

        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")

    def enable_dropdowns(self, event=None):
        if event is None:
            return

        is_win = event.value == "Win"
        cells = [[event.row, 1], [event.row, 2]]

        self.sheet.readonly_cells(cells=cells, readonly=is_win)

        if is_win:
            self.sheet.highlight_cells(cells=cells, bg="gray", fg="gray")
        else:
            self.sheet.highlight_cells(cells=cells, bg=None, fg=None)

    def get_data(self):
        if self.rows == 1:
            return [self.sheet["A1"].expand().options(header=False, index=False).data]
        else:
            return self.sheet["A1"].expand().options(header=False, index=False).data
