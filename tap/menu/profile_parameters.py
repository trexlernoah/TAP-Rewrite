import tkinter as tk
from tksheet import Sheet
from typing import List

from tap.classes import Trial


class ProfileParameters(tk.Frame):
    def __init__(
        self, master, rows: int, initial_data: List[Trial] = None, readonly=False
    ):
        self.rows = rows
        self.frame = tk.Frame(master)
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
        self.sheet.headers(["Win or Lose", "Shock", "Feedback"])

        self.sheet.dropdown(
            "A",
            values=["Win", "Lose"],
            set_value="",
            selection_function=self.enable_dropdowns,
        )
        self.sheet.dropdown("B", values=list(range(1, 11)), set_value="")
        self.sheet.dropdown("C", values=list(range(1, 11)), set_value="")

        if initial_data is not None:
            for i, trial in enumerate(initial_data):
                self.sheet[i].data = [trial.wl, trial.shock, trial.feedback]
                self.enable_dropdowns(
                    # Pass anonymous event object with value and row attributes
                    event=type("", (object,), {"value": trial.wl, "row": i})()
                )

        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")

        if readonly:
            self.sheet.disable_bindings()
            self.sheet.readonly(self.sheet["A1"].expand())

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
