from tkinter import *
import pickle

root = Tk()
root.geometry("500x400")

my_text = Text(root, width=20, height=10)
my_text.pack(pady=20)

def save_file():
    stuff = my_text.get(1.0, END)

    filename = "dat_stuff"

    output = open(filename, 'wb')

    pickle.dump(stuff, output)

def open_file():
    filename = "dat_stuff"

    input_file = open(filename, 'rb')

    stuff = pickle.load(input_file)

    my_text.insert(1.0, stuff)

my_button1 = Button(root, text="Save File", command=save_file)
my_button2 = Button(root, text="Open File", command=open_file)

my_button1.pack()
my_button2.pack()

root.mainloop()