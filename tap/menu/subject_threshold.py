import tkinter as tk

from classes import Queue, ShockTask


class SubjectThreshold(tk.Toplevel):
    def __init__(self, master, task_queue: Queue):
        self.task_queue = task_queue
        self.window = tk.Toplevel(master)

        self.window.geometry("400x300")
        self.window.title("Subject Threshold")

        subject_id_label = tk.Label(self.window, text="Subject ID")
        subject_id_label.grid(row=1, column=1)

        self.subject_id_entry = tk.Entry(self.window)
        self.subject_id_entry.grid(row=1, column=2)

        set_lower_level = tk.Label(self.window, text="Set Lower Level")
        set_lower_level.grid(row=2, column=1)

        start_lower_level = tk.Button(
            self.window,
            text="Start",
            command=self.start_low_shock,
        )
        start_lower_level.grid(row=3, column=1)

        set_higher_level = tk.Label(self.window, text="Set Higher Level")
        set_higher_level.grid(row=2, column=2)
        start_higher_level = tk.Button(
            self.window,
            text="Start",
            command=self.start_high_shock,
        )
        start_higher_level.grid(row=3, column=2)

        spacer1 = tk.Label(self.window, text="")
        spacer1.grid(row=5, column=0)

        ok = tk.Button(self.window, text="OK", command=self.write_data)
        ok.grid(row=6, column=1)

        cancel = tk.Button(
            self.window,
            text="Cancel",
            command=self.window.destroy,
        )
        cancel.grid(row=6, column=2)

    def start_low_shock(self):
        self.administer_shock(0, 1250)

    def start_high_shock(self):
        self.administer_shock(0, 2500)

    def administer_shock(self, min: int, max: int) -> int:
        def update():
            if self.task_queue.unfinished_tasks <= 0:
                return
            if self.task_queue.unfinished_tasks > len(shock_vals):
                return

            idx = len(shock_vals) - self.task_queue.unfinished_tasks
            current_shock = shock_vals[idx]
            current_shock_text.set(f"Current level: {current_shock} mA")
            progress_var.set(shock_vals[idx])
            self.window.after(500, update)

        def stop():
            self.task_queue.clear()
            subwindow.destroy()
            return current_shock

        if min < 0:
            min = 0
        if max > 2500:
            max = 2500

        subwindow = tk.Toplevel(self.window)
        subwindow.geometry("400x200")
        subwindow.resizable(False, False)
        subwindow.title("Set Threshold")

        desc = tk.Label(subwindow, text="Administering shocks")
        desc.pack(pady=20)
        # TODO maximum?
        progress_var = tk.IntVar(value=0)
        progress_bar = tk.ttk.Progressbar(
            subwindow,
            length=300,
            mode="determinate",
            maximum=max,
            variable=progress_var,
        )
        progress_bar.pack()
        # x_label_text = " | ".join("{s:.2f}".format(s=x) for x in range(0, 1201, 300))
        # x_label = tk.Label(subwindow, width=200, text=x_label_text)
        # x_label.pack()
        current_shock = 0
        current_shock_text = tk.StringVar(value=f"Current level: {current_shock} mA")
        current_shock_label = tk.Label(subwindow, textvariable=current_shock_text)
        current_shock_label.pack()
        stop_btn = tk.Button(subwindow, text="Stop", command=stop)
        stop_btn.pack()

        shock_vals = range(min, max, 75)

        for s in shock_vals:
            self.task_queue.put(ShockTask(s, 1, 4))

        update()

    def write_data(self):
        print("hi")
