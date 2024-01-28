from tkinter import *
from pynput import keyboard 
import random
from random import randint
import time

def space_key_timing():
  def on_key_release(key): #what to do on key-release
    if key == keyboard.Key.space:
      time_taken = round(time.time() - t, 2) #rounding the long decimal float
      print("The key",key," is pressed for",time_taken,'seconds')
      return False #stop detecting more key-releases

  def on_key_press(key): #what to do on key-press
    if key == keyboard.Key.space:
      return False #stop detecting more key-presses

  with keyboard.Listener(on_press = on_key_press) as press_listener: #setting code for listening key-press
      press_listener.join()

  t = time.time() #reading time in sec

  with keyboard.Listener(on_release = on_key_release) as release_listener: #setting code for listening key-release
      release_listener.join()

# Update text
# https://www.tutorialspoint.com/how-do-i-create-an-automatically-updating-gui-using-tkinter-in-python
root = Tk()
root.attributes('-fullscreen', True)
lab = Label(root)
lab = Label(root, font=("Times New Roman", 35))
lab['text'] = "Press the space bar to continue"
lab.pack()

def initial_press():
  lab['text'] = "Space bar pressed"

def press():
  def on_key_release(key): #what to do on key-release
      if key == keyboard.Key.space:
        initial_press()
        return False #stop detecting more key-releases

  def on_key_press(key): #what to do on key-press
    if key == keyboard.Key.space:
      return False #stop detecting more key-presses

  with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.start()

press()

root.mainloop()
     
# Shock Meter
# root = Tk()
#  
# cnvs = Canvas(root)
# cnvs.grid(row=0, column=0)
#  
# coord = 10, 50, 350, 350 #define the size of the gauge
#  
# # Create a background arc and a pointer (very narrow arc)
# cnvs.create_arc(coord, start=0, extent=180, fill="white",  width=2) 
# id_needle = cnvs.create_arc(coord, start= 119, extent=1, width=7)
#  
# # Add some labels
# cnvs.create_text(180,20,font="Times 20 italic bold", text="Shock Meter")
# id_text = cnvs.create_text(170,210,font="Times 15 bold")
#  
# root.mainloop()