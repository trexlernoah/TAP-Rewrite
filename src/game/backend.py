# this file should be file i/o
import pandas as pd
import main, time

def test():
    try:
        df = pd.read_csv('./src/data/eg.dat', delimiter=' ', skiprows=4)
        print(df)
    except FileNotFoundError:
        print(f"File 'eg.dat' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# tkinter should remain in ui files
from tkinter import *
from tkinter import filedialog
# As the name implies, handles everything in the backend - shock timing, saving to and reading from files, etc.

# Testing function for buttons - to be removed
def example():
    print("Example")

# Format is as follows: "<attribute name>=<value>"
# Ex: To create an attribute "test" with value 5 in file "test-experiment", do the following:
# append_variable("test", 5, "test-experiment")
def append_variable(name, value, filename=None):
    if filename is None:
        filename="default"

    experment_file = open(filename+".txt", "a+")
    experment_file.write(name + "=" + str(value) + "\n")
    experment_file.close()

# Note: need to specify complete string for this to work (ex: "test=5" rather than just "5")
def update_variable(name, new_value, filename=None):
    if filename is None:
        filename="default"
    
    f = open(filename+".txt", 'r')
    filedata = f.read()
    f.close()

    # Bit of code for finding and replacing the old value with a new value.
    # I have no idea why this must be so specific to work but it does.
    old_value = filedata.split(name+'=')[1].split('\n')[0]
    newdata = filedata.replace(name+"="+old_value, name+"="+str(new_value))

    f = open(filename+".txt",'w')
    f.write(newdata)
    f.close()

# Usage example:
# read_variable("<attribute name", "<filename>")
def read_variable(name, filename=None):
    if filename is None:
        print("Error: no filename specified")
        return None

    f = open(filename+".txt", 'r')
    filedata = f.read()
    f.close()
    
    # return *only* the value of the specified attribute
    result = filedata.split(name+'=')[1].split('\n')[0]
    return result

# Initialize a new experiment template - autofill options with defaults, etc.
def init_experiment(filename="default"):    
    # Values to initialize a new experiment file
    # Set experiment ID as the name of the filename by default
    default_filename = "subject_id=experiment\n"
    subject_threshold = "subject_low_threshold=0.000\nsubject_high_threshold=0.000\n"
    default_pulse_increments = "\npulse_increments=7.5\n"
    RCAP_config = "\nIf response_options_config is set to 0, then 0_10 is enabled (RCAP is on).\nIf not, 1_10 is enabled (RCAP is off).\nresponse_options_config=1\n"
    delay = "\ndelay=50\ndelay_between_shocks=2500\nshock_duration=1000"
    number_of_trials = "\ntrials=3\n"

    # Bit of code for writing "Corresponding Interval" sections to the file
    # This is easier than having a massive string of values.
    main = ''.join([default_filename, subject_threshold, default_pulse_increments, RCAP_config])

    for i in range (10):
        main += "\ncorresponding_interval_" + str(i) + "=" + str((55 + i*5))

    main += delay
    main += number_of_trials

    f = open(filename+".txt", "w")
    f.write(main)
    f.close()

# Open a file
def open_experiment():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    return filename

def save_data(data: pd.DataFrame, filename: str):
    if not filename: return
    data.to_csv(filename, sep=' ', encoding='utf-8', index=False)

# Fix
# Fill with variables later
# def data_sheet():
#     from docx import Document

# Just testing
# init_experiment("experiment")
# update_variable("subject_low_threshold", 1.00, "experiment")
# update_variable("subject_high_threshold", 2.00, "experiment")
# update_variable("corresponding_interval_0", 2.054, "experiment")
def run_official(trials: int):
    if trials == 0: return
    data = main.main(trials)
    # throw error here
    if data.empty: return
    print(data)
    data.columns = ['Trial', 'W/L', 'Shock', 'Duration', 'ReactionTime']
    filename = time.strftime("%Y%m%d-%H%M%S")
    save_data(data, './src/data/%s.dat' % filename)