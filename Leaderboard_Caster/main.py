#import keyboard
from tkinter import *
from screeninfo import get_monitors
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import sys
import time
from threading import Timer

time.sleep(2)

#Gets scrren information eg screen seize
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height



#Starts a new window
window = Tk()


#Sets the seize of window
window.geometry(f'{screen_width}x{screen_height}')
window.attributes("-fullscreen", True)
window.configure(bg="Red")


window.mainloop()

print("hwef")
exec(open(r"C:\Users\axlindm\PycharmProjects\Leadweboard2\race_handler.py").read())
time.sleep(2)
    #exec(open("race_handler.py").read())




















