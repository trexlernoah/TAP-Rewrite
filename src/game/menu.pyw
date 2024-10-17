import os
import pickle
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

import game
import constants
from profile_parameters import ProfileParameters
from utils import Trial, validate_data


class main_menu:
    """Tkinter menu class"""

    def __init__(self) -> None:
        window = tk.Tk()
        window.title("TAP Python Edition")
        window.geometry("500x500")
        window.resizable(width=True, height=True)

        self.window = window
        self.state = constants.initial_state

    def create_new_instruction(self, instruction="Enter instructions here"):
        def ok():
            self.state["instruction"] = instruction_text.get("1.0", tk.END)
            print(self.state["instruction"])
            new_instruction.destroy()

        def cancel():
            new_instruction.destroy()

        def clear():
            instruction_text.delete("1.0", tk.END)

        new_instruction = tk.Toplevel(self.window)
        new_instruction.title("Instructions")
        new_instruction.resizable(False, False)

        new_instruction.rowconfigure(0, minsize=400, weight=1)
        new_instruction.columnconfigure(0, minsize=200, weight=1)

        instruction_text = tk.Text(new_instruction)
        btn_frame = tk.Frame(new_instruction, bd=2)

        ok_btn = tk.Button(btn_frame, text="Ok", command=ok)
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=cancel)
        clear_btn = tk.Button(btn_frame, text="Clear Text", command=clear)

        ok_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        cancel_btn.grid(row=1, column=0, sticky="ew", padx=5)
        clear_btn.grid(row=3, column=0, sticky="ew", padx=5, pady=20)

        instruction_text.grid(row=0, column=0, sticky="nsew")
        btn_frame.grid(row=0, column=1, sticky="ns")

        instruction_text.insert("1.0", instruction)

    def run_official(self, trials):
        if len(trials) == 0:
            return
        data = game.play(self.state["subject_id"], trials)
        df = data.get_data_frame()
        # throw error here
        if df.empty:
            return
        # filename = time.strftime("%Y%m%d-%H%M%S")
        # data.save_data('%s/data/%s.dat' % (os.getcwd(), filename))
        data.save_data("%s/data/%s.dat" % (os.getcwd(), self.state["subject_id"]))

    def run_experiment(self):
        if len(self.state["trials"]) <= 0:
            messagebox.showinfo(
                title="Warning", message="You must set the number of trials!"
            )
            return
        self.run_official(self.state["trials"])

    def show_about_info(self):
        messagebox.showinfo(
            title="About",
            message="This is a rewrite of the TAP software in Python using the NI DAQ USB-6001 Module.",
        )

    def set_options(self):
        options = tk.Toplevel(self.window)
        options.geometry("400x200")
        options.title("Options")

        options_tab = ttk.Notebook(options)
        threshold_options = ttk.Frame(options_tab)
        timing_options = ttk.Frame(options_tab)

        options_tab.add(threshold_options, text="Threshold Options")
        options_tab.add(timing_options, text="Timing")

    def set_subject_threshold(self):
        if not self.state["trials"]:
            messagebox.showinfo(
                title="Error", message="You must open an experiment first."
            )
            return

        subject_threshold = tk.Toplevel(self.window)
        subject_threshold.geometry("300x200")
        subject_threshold.resizable(False, False)
        subject_threshold.title("Subject Threshold")

        subject_id = tk.Label(subject_threshold, text="Subject ID")
        subject_id.grid(row=1, column=1)

        subject_id_entry = tk.Entry(subject_threshold)
        subject_id_entry.grid(row=1, column=2)

        set_lower_level = tk.Label(subject_threshold, text="Set Lower Level")
        set_lower_level.grid(row=2, column=1)

        # Just gonna leave the code for controlling the shock here
        # Boolean for stopping the shock function
        # global low_stopped, low_mA, high_stopped, high_mA
        low_stopped = False
        high_stopped = False
        low_mA = 0.10
        high_mA = 0.15

        def start_low_shock():
            nonlocal low_mA, low_stopped
            while low_mA <= 0.50 and not low_stopped:
                if low_stopped:
                    print("Stopping low")
                    break
                # daq.test(low_mA, 1000)
                low_mA = low_mA + 0.075
                print("Administered shock of " + str(low_mA) + " milliamps.")
            print("Returning shock of " + str(low_mA) + " milliamps.")

        def stop_low_shock():
            nonlocal low_stopped
            low_stopped = True
            print("Stopping lower threshold.")

        def low_button_starter():
            t = threading.Thread(target=start_low_shock)
            t.start()

        def start_high_shock():
            nonlocal high_mA, high_stopped
            print("Starting higher threshold.")
            while high_mA <= 1.00 and not high_stopped:
                if high_stopped:
                    print("Stopping high")
                    break
                # daq.test(high_mA, 1000)
                high_mA = high_mA + 0.075
                print("Administered shock of " + str(high_mA) + " milliamps.")
            print("Returning shock of " + str(high_mA) + " milliamps.")

        def stop_high_shock():
            nonlocal high_stopped
            high_stopped = True
            print("Stopping higher threshold.")

        def high_button_starter():
            t = threading.Thread(target=start_high_shock)
            t.start()

        def write_data():
            nonlocal low_mA, high_mA
            # TODO apply low/high shocks to threshold
            id_num = subject_id_entry.get()
            self.state["subject_id"] = str(id_num)
            subject_threshold.destroy()

        start_lower_level = tk.Button(
            subject_threshold,
            relief="groove",
            text="Start",
            padx=10,
            pady=10,
            command=low_button_starter,
        )
        start_lower_level.grid(row=3, column=1)
        stop_lower_level = tk.Button(
            subject_threshold,
            relief="groove",
            text="Stop",
            padx=10,
            pady=10,
            command=stop_low_shock,
        )
        stop_lower_level.grid(row=4, column=1)

        set_higher_level = tk.Label(subject_threshold, text="Set Higher Level")
        set_higher_level.grid(row=2, column=2)
        start_higher_level = tk.Button(
            subject_threshold,
            relief="groove",
            text="Start",
            padx=10,
            pady=10,
            command=high_button_starter,
        )
        start_higher_level.grid(row=3, column=2)
        stop_higher_level = tk.Button(
            subject_threshold,
            relief="groove",
            text="Stop",
            padx=10,
            pady=10,
            command=stop_high_shock,
        )
        stop_higher_level.grid(row=4, column=2)

        spacer1 = tk.Label(subject_threshold, text="")
        spacer1.grid(row=5, column=0)

        # Fix
        # Return values of lower and higher number (just a matter of using the append() function and returning the low and high functions)
        ok = tk.Button(
            subject_threshold, relief="groove", text="OK", command=write_data
        )
        ok.grid(row=6, column=1)

        cancel = tk.Button(
            subject_threshold,
            relief="groove",
            text="Cancel",
            command=subject_threshold.destroy,
        )
        cancel.grid(row=6, column=2)

    def get_trial_count(self):
        number_of_trials = simpledialog.askinteger(
            "Profile Setup", "Number of Trials: "
        )

        # Fix
        # Checkbox for "Enable RCAP"
        # rcap_checkbox = tk.Checkbutton(window, text='Enable RCAP',variable=var1, onvalue=1, offvalue=0, command=print_selection)
        # rcap_checkbox.grid(row=1, column=4)
        # self.state['trial-count'] = number_of_trials if not None else 0
        # update_variable("trials", number_of_trials, "experiment")

        if number_of_trials is not None:
            self.state["trial_count"] = number_of_trials
            self.profile_parameters()

    def profile_parameters(self, edit=False):
        def ok():
            try:
                data = profile_parameters_window.get_data()

                for i in range(0, trial_count):
                    trial = validate_data(data[i])
                    if not trial:
                        raise ValueError("Malformed data.")
                    self.state["trials"].append(Trial(data[i]))

                profile_parameters_window.destroy()
            except ValueError:
                messagebox.showinfo(
                    title="Error",
                    message="There was an error creating the trials. Check your entries again.",
                )

        trial_count = self.state["trial_count"]
        if not trial_count or trial_count <= 0:
            return

        profile_parameters_window = ProfileParameters(self.window, trial_count)

        ok_btn = tk.Button(
            profile_parameters_window,
            text="Ok",
            command=ok,
        )
        ok_btn.grid(row=trial_count + 2, column=0)

    def save_experiment(self):
        files = [("TAP files", "*.tap"), ("All files", "*.*")]
        file = filedialog.asksaveasfile(
            mode="wb",
            filetypes=files,
            initialfile=self.state["filename"],
            defaultextension=".tap",
        )
        if file is None:
            return
        try:
            self.state["filename"] = file.name
            pickle.dump(self.state, file)
            file.close()
        except Exception:
            messagebox.showinfo(
                title="Error", message="There was an error saving the file."
            )

    def open_experiment(self):
        filetypes = [("TAP files", "*.tap"), ("All files", "*.*")]
        file = filedialog.askopenfile(
            mode="rb", filetypes=filetypes, defaultextension=".tap"
        )
        if file is None:
            return
        try:
            self.state = pickle.load(file)
            self.state["filename"] = file.name
        except Exception:
            messagebox.showinfo(
                title="Error", message="There was an error opening the file."
            )

    def edit_experiment(self):
        # if self.state[]
        print("")

    def init_main_window(self):
        # Cofigure sizing for rows and columns
        self.window.rowconfigure(1, minsize=800, weight=1)
        self.window.columnconfigure(0, minsize=800, weight=1)

        main = tk.Frame(self.window)
        main.pack(fill="both", expand=True, padx=1, pady=(4, 0))

        # Add menu bar
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # Add menu options in menu bar
        # Names should be fairly self explanitory
        experiment_menu = tk.Menu(menubar, tearoff=0)
        open_experiment_menu = tk.Menu(menubar, tearoff=0)
        create_new_menu = tk.Menu(menubar, tearoff=0)
        edit_current_menu = tk.Menu(experiment_menu, tearoff=0)
        run_menu = tk.Menu(experiment_menu, tearoff=0)

        # Create main menu
        threshold_menu = tk.Menu(menubar, tearoff=0)

        # Main menu options
        menubar.add_cascade(menu=experiment_menu, label="Experiment")
        menubar.add_cascade(menu=threshold_menu, label="Threshold")
        menubar.add_command(label="About", command=self.show_about_info)

        # Experiment dropdown menu options
        experiment_menu.add_cascade(label="Create New", menu=create_new_menu)
        # Open experiment
        experiment_menu.add_command(
            label="Open Experiment", command=self.open_experiment
        )

        # "Create New" dropdown menu options
        create_new_menu.add_command(
            label="Instruction", command=self.create_new_instruction
        )
        create_new_menu.add_command(label="Experiment", command=self.get_trial_count)

        # "Edit Current" dropdown menu options
        experiment_menu.add_cascade(label="Edit Current", menu=edit_current_menu)
        edit_current_menu.add_command(
            label="Instruction",
            command=lambda: self.create_new_instruction(self.state["instruction"]),
        )
        edit_current_menu.add_command(
            label="Experiment", command=lambda: self.profile_parameters(edit=True)
        )
        experiment_menu.add_separator()

        # "Save Experiment" dropdown menu option
        experiment_menu.add_command(
            label="Save Experiment", command=self.save_experiment
        )
        experiment_menu.add_separator()

        # Run dropdown menu options
        experiment_menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Practice")
        run_menu.add_command(label="Official", command=self.run_experiment)
        experiment_menu.add_separator()

        # Exit dropdown menu option
        experiment_menu.add_command(label="Exit", command=self.window.destroy)

        # Threshold dropdown menu options
        threshold_menu.add_command(
            label="Set Subject Threshold", command=self.set_subject_threshold
        )
        threshold_menu.add_command(label="Options")

        # About dropdown menu option
        # about_menu.add_command(label="About", command=show_about_info)

        # Start menu
        self.window.mainloop()


menu = main_menu()
menu.init_main_window()
