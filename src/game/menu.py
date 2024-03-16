import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog

# Import shock function
# from shock import *

# Global variables 
from backend import *

# Create and initialize new window


class main_menu():
    '''Tkinter menu class'''
    def __init__(self) -> None:
        window = tk.Tk()
        window.title("TAP Python Edition")
        window.geometry("500x500")
        window.resizable(width=True, height=True)

        self.window = window
    
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
        
        update_variable("trials", number_of_trials, "experiment")
        if number_of_trials != None:
            for i in range(number_of_trials):
                append_variable("trial-"+str(i), number_of_trials, "experiment")
            # self.profile_parameters(trial_num=number_of_trials)
        else:
            number_of_trials=0


    def profile_parameters(self, trial_num):
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
        experiment_menu.add_cascade(label="Open Experiment", command=open_experiment)

        # "Create New" dropdown menu options
        create_new_menu.add_command(label="Instruction", command=example)
        create_new_menu.add_command(label="Experiment", command=lambda:[init_experiment("experiment"), self.profile_setup()])
        experiment_menu.add_separator()

        # "Edit Current" dropdown menu options
        experiment_menu.add_cascade(label="Edit Current", menu=edit_current_menu)
        edit_current_menu.add_command(label="Instruction", command=example)
        edit_current_menu.add_command(label="Experiment", command=example)
        experiment_menu.add_separator()

        # "Save Experiment" dropdown menu option
        experiment_menu.add_command(label="Save Experiment", command=example)
        experiment_menu.add_separator()

        # Run dropdown menu options
        experiment_menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Practice", command=example)
        run_menu.add_command(label="Official", command=run_official)
        experiment_menu.add_separator()

        # Exit dropdown menu option
        experiment_menu.add_command(label="Exit", command=self.window.destroy)

        # Threshold dropdown menu options
        threshold_menu.add_command(label="Set Subject Threshold", command=self.set_subject_threshold)

        # About dropdown menu option
        # about_menu.add_command(label="About", command=show_about_info)

        # Start menu
        self.window.mainloop()

menu = main_menu()
menu.init_main_window()