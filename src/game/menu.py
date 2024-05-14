import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog

import pickle

# Import shock function
# from shock import *

# Global variables 
from backend import *

# Create and initialize new window

class Trial(object):
    def __init__(self, wl, shock, feedback):
        self.wl = wl
        self.shock = shock
        self.feedback = feedback

# Initial state (move to const file)
state = {'instruction': "Enter instructions here",
         'trial-count': 0,
         'trials': []}

class main_menu():
    '''Tkinter menu class'''
    def __init__(self) -> None:
        window = tk.Tk()
        window.title("TAP Python Edition")
        window.geometry("500x500")
        window.resizable(width=True, height=True)

        self.window = window
        self.state = state
    
    def create_new_instruction(self):
        def ok():
            self.state['instruction'] = instruction_text.get("1.0", tk.END)
            print(self.state['instruction'])
            new_instruction.destroy()
        def cancel():
            new_instruction.destroy()
        def clear():
            instruction_text.delete("1.0", tk.END)

        new_instruction = Toplevel(self.window)
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

        instruction_text.insert("1.0", self.state['instruction'])

    def run_experiment(self):
        print(self.state['trials'][0])
        if len(self.state['trials']) <= 0:
            messagebox.showinfo(
                title="Warning",
                message="You must set the number of trials!"
            )
            return
        run_official(self.state['trials'])

    def show_about_info(self):
        messagebox.showinfo(
            title="About",
            message="This is a rewrite of the TAP software in Python using the NI DAQ USB-6001 Module."
        )

    def set_options(self):
        options = Toplevel(self.window)
        options.geometry("400x200")
        options.title("Options")

        options_tab = ttk.Notebook(options)
        threshold_options = ttk.Frame(options_tab)
        timing_options = ttk.Frame(options_tab)

        options_tab.add(threshold_options, text="Threshold Options")
        options_tab.add(timing_options, text="Timing")

    def set_subject_threshold(self):
        subject_threshold = Toplevel(self.window)
        subject_threshold.geometry("300x200")
        subject_threshold.resizable(False, False)
        subject_threshold.title("Subject Threshold")

        subject_id = tk.Label(subject_threshold, text="Subject ID")
        subject_id.grid(row=1, column=1)

        subject_id_entry = tk.Entry(subject_threshold)
        subject_id_entry.grid(row=1, column=2)
        id_num = subject_id_entry.get()
        update_variable("experiment_id", str(id_num), "experiment")
        # update_variable("experiment_id", '001', "experiment")

        set_lower_level = tk.Label(subject_threshold, text="Set Lower Level")
        set_lower_level.grid(row=2, column=1)

        # Just gonna leave the code for controlling the shock here
        # Boolean for stopping the shock function
        low_running = False
        high_running = False
        i = 0.10
        j = 0.15

        def start_low_shock():
            global low_running
            global i
            low_running = False 
            print("Starting lower threshold.")
            # Increment the shock up from 0.10 by 0.05, with a limit of 4
            # Numbers are in milliamps, in case not clear.
            i = 0.10
            while i <= 3 and not low_running:
                if low_running:
                    break
                else:
                    # analog_out(i, 2)
                    i = i + 0.5
                    print("Administered shock of " + str(i) + " milliamps.")

            print("Returning shock of " + str(i) + " milliamps.")
            return i

        def stop_low_shock():
            global low_running
            low_running = True
            print("Stopping lower threshold.")

        def low_button_starter():
            t = threading.Thread(target=start_low_shock)
            t.start()

        def start_high_shock():
            global high_running
            global j
            high_running = False
            print("Starting higher threshold.")
            # Increment the shock up from 0.10 by 0.05, with a limit of 4
            # Numbers are in milliamps, in case not clear.
            j = 0.15
            while j <= 3 and not high_running:
                if high_running:
                    break
                else:
                    # analog_out(i, 2)
                    j = j + 0.5
                    print("Administered shock of " + str(j) + " milliamps.")

            print("Returning shock of " + str(j) + " milliamps.")
            return j

        def stop_high_shock():
            global high_running
            high_running = True 
            print("Stopping higher threshold.")

        def high_button_starter():
            t = threading.Thread(target=start_high_shock)
            t.start()

        def write_data():
            global i
            global j
            update_variable("subject_low_threshold", str(i), "experiment")
            print("Writing low shock of " + str(i) + " milliamps to file")
            update_variable("subject_high_threshold", str(j), "experiment")
            print("Writing high shock of " + str(j) + " milliamps to file")

        start_lower_level = tk.Button(subject_threshold, relief='groove', text="Start", padx=10, pady=10, command=low_button_starter)
        start_lower_level.grid(row=3, column=1)
        stop_lower_level = tk.Button(subject_threshold, relief='groove', text="Stop", padx=10, pady=10,command=stop_low_shock)
        stop_lower_level.grid(row=4, column=1)
    
        set_higher_level = tk.Label(subject_threshold, text="Set Higher Level")
        set_higher_level.grid(row=2, column=2)
        start_higher_level= tk.Button(subject_threshold, relief='groove', text="Start", padx=10, pady=10,command=high_button_starter)
        start_higher_level.grid(row=3, column=2)
        stop_higher_level= tk.Button(subject_threshold, relief='groove', text="Stop", padx=10, pady=10,command=stop_high_shock)
        stop_higher_level.grid(row=4, column=2)

        spacer1 = tk.Label(subject_threshold, text="")
        spacer1.grid(row=5, column=0)

        # Fix
        # Return values of lower and higher number (just a matter of using the append() function and returning the low and high functions)
        ok = tk.Button(subject_threshold, relief='groove', text="OK", command=write_data)
        ok.grid(row=6, column=1)

        cancel = tk.Button(subject_threshold, relief='groove', text="Cancel", command=subject_threshold.destroy)
        cancel.grid(row=6, column=2)

    def profile_setup(self):
        number_of_trials = simpledialog.askinteger("Profile Setup", "Number of Trials: ")
        
        # Fix
        # Checkbox for "Enable RCAP"
        # rcap_checkbox = tk.Checkbutton(window, text='Enable RCAP',variable=var1, onvalue=1, offvalue=0, command=print_selection)
        # rcap_checkbox.grid(row=1, column=4) 
        # self.state['trial-count'] = number_of_trials if not None else 0
        # update_variable("trials", number_of_trials, "experiment")
        if number_of_trials != None:
            for i in range(number_of_trials):
                append_variable("trial-"+str(i), number_of_trials, "experiment")
            self.profile_parameters(trial_num=number_of_trials)
        else:
            number_of_trials=0


    def profile_parameters(self, trial_num: int):
        def ok(wl, entries):
            trials = []
            for i in range(1, len(entries)):
                # res.append()
                # self.state['trials']
                print(wl[i-1].get())
                print(entries[i][2].get())
                print(entries[i][3].get())
                trials.append(Trial(wl[i-1].get(), 
                                    entries[i][2].get(), 
                                    entries[i][3].get()))
            self.state['trials'] = trials
            profile_parameters.destroy()

        if not trial_num: return
        profile_parameters = Toplevel(self.window)
        profile_parameters.geometry("600x400")
        profile_parameters.title("Setup Profile Parameters")

        profile_parameters.grid_rowconfigure(0, weight=1)
        profile_parameters.columnconfigure(0, weight=1)

        grid_frame = tk.Frame(profile_parameters)
        grid_frame.grid(row=0, column=0, pady=(5,0), sticky="nw")
        grid_frame.grid_rowconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_propagate(False)

        canvas = tk.Canvas(grid_frame, bg="white")
        canvas.grid(row=0, column=0, sticky="news")

        vsb = tk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_buttons = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        rows = trial_num + 1
        columns = 4
        print(rows, columns)
        entries = [[tk.Entry() for j in range(columns)] for i in range(rows)]
        # wl = tk.StringVar(self.window)

        wl = []

        label1 = tk.Label(frame_buttons, text="Win or Lose")
        label1.grid(row=0, column=1, sticky='news')
        label2 = tk.Label(frame_buttons, text="Shock")
        label2.grid(row=0, column=2, sticky='news')
        label3 = tk.Label(frame_buttons, text="Feedback")
        label3.grid(row=0, column=3, sticky='news')

        for i in range(1, rows):
            wl.append(tk.StringVar())

            entries[i][0] = tk.Label(frame_buttons, text=("Trial %d" % i))
            entries[i][0].grid(row=i, column=0, sticky='news')

            entries[i][1] = tk.OptionMenu(frame_buttons, wl[i-1], *('Win', 'Lose'))
            entries[i][1].grid(row=i, column=1, sticky='news')
            entries[i][2] = tk.Entry(frame_buttons)
            entries[i][2].grid(row=i, column=2, sticky='news')
            entries[i][3] = tk.Entry(frame_buttons)
            entries[i][3].grid(row=i, column=3, sticky='news')

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        # first4columns_width = sum([entries[0][j].winfo_width() for j in range(0, 4)])
        # first5rows_height = sum([entries[i][0].winfo_height() for i in range(0, (rows if rows < 5 else 5))])
        grid_frame.config(width=600 + vsb.winfo_width(),
                            height=200)

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

        ok_btn = tk.Button(profile_parameters, text="Ok", command=lambda : ok(wl, entries))
        ok_btn.grid(row=rows+1, column=0)

    def x_profile_parameters(self, trial_num):
        profile_parameters = Toplevel(self.window)
        profile_parameters.geometry("500x300")
        profile_parameters.title("Setup Profile Parameters")

        # Initialize array of trial elements for later
        ref = []
        for i in range(trial_num):
            trial = tk.Label(profile_parameters, text="Trial "+str(i+1))
            trial.grid(row=i, column=0)

            shock_duration_label = tk.Label(profile_parameters, text="Shock Duration: ")
            shock_duration_label.grid(row=i, column=1)
            shock_duration = Entry(profile_parameters)
            
            # Hardcoding the default shock value because having issues parsing it out of the .txt file
            shock_duration.insert(0, 1000)
            shock_duration.grid(row=i, column=2)

            ref.append(trial)
        
        def check_shock_output():
            done=False
            for i in ref:
                if(len(i.get()) < 0):
                    done=True

            if (done == False):
                print("Done")
            else:
                print("Not done")
            
        # Fix
        # Use a for loop and this article: https://stackoverflow.com/questions/15801199/tkinter-addressing-label-widget-created-by-for-loop
        # to generate Trial labels as needed

    
# label = Label(profile_options)
# label.grid(row=2, column=1)

    def save_experiment(self):
        files = [('TAP files', '*.tap'),
                 ('All files', '*.*')]
        file = filedialog.asksaveasfile(mode="wb", filetypes=files, defaultextension='.tap')
        if file is None:
            return
        try:
            pickle.dump(self.state, file)
            file.close()
        except:
            messagebox.showinfo(
                title="Error",
                message="There was an error opening the file."
            )

    def open_experiment(self):
        files = [('TAP files', '*.tap'),
                 ('All files', '*.*')]
        file = filedialog.askopenfile(mode="rb", filetypes=files, defaultextension='.tap')
        if file is None:
            return
        try:
            self.state = pickle.load(file)
        except:
            messagebox.showinfo(
                title="Error",
                message="There was an error opening the file."
            )

### Window Management

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
        experiment_menu.add_command(label="Open Experiment", command=self.open_experiment)

        # "Create New" dropdown menu options
        create_new_menu.add_command(label="Instruction", command=self.create_new_instruction)
        create_new_menu.add_command(label="Experiment", command=lambda:[init_experiment("experiment"), self.profile_setup()])

        # "Edit Current" dropdown menu options
        experiment_menu.add_cascade(label="Edit Current", menu=edit_current_menu)
        edit_current_menu.add_command(label="Instruction", command=example)
        edit_current_menu.add_command(label="Experiment", command=example)
        experiment_menu.add_separator()

        # "Save Experiment" dropdown menu option
        experiment_menu.add_command(label="Save Experiment", command=self.save_experiment)
        experiment_menu.add_separator()

        # Run dropdown menu options
        experiment_menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Practice", command=example)
        run_menu.add_command(label="Official", command=self.run_experiment)
        experiment_menu.add_separator()

        # Exit dropdown menu option
        experiment_menu.add_command(label="Exit", command=self.window.destroy)

        # Threshold dropdown menu options
        threshold_menu.add_command(label="Set Subject Threshold", command=self.set_subject_threshold)
        threshold_menu.add_command(label="Options", command=example)

        # About dropdown menu option
        # about_menu.add_command(label="About", command=show_about_info)

        # Start menu
        self.window.mainloop()

menu = main_menu()
menu.init_main_window()