import threading, pickle, os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

import main, constants
from utils import *

class main_menu():
    '''Tkinter menu class'''
    def __init__(self) -> None:
        window = tk.Tk()
        window.title("TAP Python Edition")
        window.geometry("500x500")
        window.resizable(width=True, height=True)

        self.window = window
        self.state = constants.initial_state
    
    def create_new_instruction(self, instruction="Enter instructions here"):
        def ok():
            self.state['instruction'] = instruction_text.get("1.0", tk.END)
            print(self.state['instruction'])
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
        if len(trials) == 0: return
        data = main.main(self.state['subject_id'], trials)
        df = data.get_data_frame()
        # throw error here
        if df.empty: return
        print(df)
        # filename = time.strftime("%Y%m%d-%H%M%S")
        # data.save_data('%s/data/%s.dat' % (os.getcwd(), filename))
        data.save_data('%s/data/%s.dat' % (os.getcwd(), self.state['subject_id']))

    def run_experiment(self):
        print(self.state['trials'][0])
        if len(self.state['trials']) <= 0:
            messagebox.showinfo(
                title="Warning",
                message="You must set the number of trials!"
            )
            return
        self.run_official(self.state['trials'])

    def show_about_info(self):
        messagebox.showinfo(
            title="About",
            message="This is a rewrite of the TAP software in Python using the NI DAQ USB-6001 Module."
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
        if not self.state['trials']:
            messagebox.showinfo(
                title="Error",
                message="You must open an experiment first."
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
        # update_variable("experiment_id", str(id_num), "experiment")
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
            # global i
            # global j
            # update_variable("subject_low_threshold", str(i), "experiment")
            # print("Writing low shock of " + str(i) + " milliamps to file")
            # update_variable("subject_high_threshold", str(j), "experiment")
            # print("Writing high shock of " + str(j) + " milliamps to file")
            id_num = subject_id_entry.get()
            self.state['subject_id'] = str(id_num)
            subject_threshold.destroy()

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
            # for i in range(number_of_trials):
                # append_variable("trial-"+str(i), number_of_trials, "experiment")
            self.state['trial_count'] = number_of_trials
            self.profile_parameters()
        else:
            number_of_trials=0


    def profile_parameters(self, edit=False):
        def ok(wl, shocks, entries):
            try:
                trials = []
                for i in range(1, len(entries)):
                    # res.append()
                    # self.state['trials']
                    print('here')
                    print(shocks[i-1].get())
                    print(wl[i-1].get())
                    print(shocks[i-1].get())
                    print(entries[i][3].get())
                    trials.append(Trial(wl[i-1].get(), 
                                        shocks[i-1].get(), 
                                        entries[i][3].get()))
                self.state['trials'] = trials
                profile_parameters.destroy()
            except:
                messagebox.showinfo(
                    title="Error",
                    message="There was an error creating the trials."
                )

        trial_num = self.state['trial_count']
        if not trial_num: return

        profile_parameters = tk.Toplevel(self.window)
        profile_parameters.geometry("400x300")
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
        shock_vars = []
        numbers = list(range(1,11))

        label1 = tk.Label(frame_buttons, text="Win or Lose")
        label1.grid(row=0, column=1, sticky='news')
        label2 = tk.Label(frame_buttons, text="Shock")
        label2.grid(row=0, column=2, sticky='news')
        label3 = tk.Label(frame_buttons, text="Feedback")
        label3.grid(row=0, column=3, sticky='news')

        def insert_text(idx: int, wl_var, shock, feedback):
            trials = self.state['trials']
            if len(trials) == 0: return
    
            trial: Trial = trials[idx]
            print(trial.wl, trial.shock, trial.feedback)
            wl_var.set(str(trial.wl))
            if wl_var.get() == 'Lose':
                shock.configure(state='normal')
                feedback.configure(state='normal')
                # shock.set(numbers[0])
                # shock.delete(0,tk.END)
                # shock.insert(0,str(trial.shock))
                feedback.delete(0,tk.END)
                feedback.insert(0,str(trial.feedback))
            else:
                shock.configure(state='disabled')
                feedback.configure(state='disabled')

        row_entries = {}

        for i in range(1, rows):
            row_name = 'wl'+str(i-1)
            shock_var = tk.StringVar() 
            # shock_var.set(numbers[0])
            shock_entry = tk.OptionMenu(frame_buttons, shock_var, *numbers)
            feedback_entry = tk.Entry(frame_buttons)
            def is_disabled(*args):
                print(args)
                print(row_entries)
                try:
                    wl = row_entries.get(args[0])
                    if wl[0].get() == 'Lose':
                        wl[1].configure(state='normal')
                        wl[2].configure(state='normal')
                    else:
                        wl[1].configure(state='disabled')
                        wl[2].configure(state='disabled')
                except:
                    print('nope')
            
            wl_var = tk.StringVar(name=row_name)
            wl_var.trace_add('write', is_disabled)
            wl.append(wl_var)
            shock_vars.append(shock_var)

            entries[i][0] = tk.Label(frame_buttons, text=("Trial %d" % i))
            entries[i][0].grid(row=i, column=0, sticky='news')

            entries[i][1] = tk.OptionMenu(frame_buttons, wl_var, *('Win', 'Lose'))
            entries[i][1].grid(row=i, column=1, sticky='news')
            entries[i][2] = shock_entry
            entries[i][2].grid(row=i, column=2, sticky='news')
            entries[i][3] = feedback_entry
            entries[i][3].grid(row=i, column=3, sticky='news')

            row_entries[row_name] = [wl_var, shock_entry, feedback_entry]

            if edit: insert_text(i-1, wl_var, shock_entry, feedback_entry)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        # first4columns_width = sum([entries[0][j].winfo_width() for j in range(0, 4)])
        # first5rows_height = sum([entries[i][0].winfo_height() for i in range(0, (rows if rows < 5 else 5))])
        height = entries[i][0].winfo_height() * 5
        grid_frame.config(width=330+vsb.winfo_width(), height=height)

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

        ok_btn = tk.Button(profile_parameters, text="Ok", command=lambda : ok(wl, shock_vars, entries))
        ok_btn.grid(row=rows+1, column=0)

    def save_experiment(self):
        files = [('TAP files', '*.tap'),
                 ('All files', '*.*')]
        file = filedialog.asksaveasfile(mode="wb", 
                                        filetypes=files, 
                                        initialfile=self.state['filename'], 
                                        defaultextension='.tap')
        if file is None:
            return
        try:
            self.state['filename'] = file.name
            pickle.dump(self.state, file)
            file.close()
        except:
            messagebox.showinfo(
                title="Error",
                message="There was an error saving the file."
            )

    def open_experiment(self):
        files = [('TAP files', '*.tap'),
                 ('All files', '*.*')]
        file = filedialog.askopenfile(mode="rb", filetypes=files, defaultextension='.tap')
        if file is None:
            return
        try:
            self.state = pickle.load(file)
            self.state['filename'] = file.name
        except:
            messagebox.showinfo(
                title="Error",
                message="There was an error opening the file."
            )       
    
    def edit_experiment(self): 
        # if self.state[]
        print("")

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
        create_new_menu.add_command(label="Experiment", command=self.profile_setup)

        # "Edit Current" dropdown menu options
        experiment_menu.add_cascade(label="Edit Current", menu=edit_current_menu)
        edit_current_menu.add_command(label="Instruction", command=lambda:self.create_new_instruction(self.state['instruction']))
        edit_current_menu.add_command(label="Experiment", command=lambda:self.profile_parameters(edit=True))
        experiment_menu.add_separator()

        # "Save Experiment" dropdown menu option
        experiment_menu.add_command(label="Save Experiment", command=self.save_experiment)
        experiment_menu.add_separator()

        # Run dropdown menu options
        experiment_menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Practice")
        run_menu.add_command(label="Official", command=self.run_experiment)
        experiment_menu.add_separator()

        # Exit dropdown menu option
        experiment_menu.add_command(label="Exit", command=self.window.destroy)

        # Threshold dropdown menu options
        threshold_menu.add_command(label="Set Subject Threshold", command=self.set_subject_threshold)
        threshold_menu.add_command(label="Options")

        # About dropdown menu option
        # about_menu.add_command(label="About", command=show_about_info)

        # Start menu
        self.window.mainloop()

menu = main_menu()
menu.init_main_window()