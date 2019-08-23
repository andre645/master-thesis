import sys, os, threading, serial, time
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil


path = os.getcwd()+"\\RunMe"
if os.path.isdir(path) is True:
    shutil.rmtree(path) 
   
os.mkdir(path)

main_win = tkinter.Tk()
main_win.title("Select Vg sweep parameters")
main_win.geometry("500x500")

def cyclesnumber():
    global cycles 
    cycles = cyclesentry.get()
    return cycles


def stepsnumber():
    global steps
    steps = stepsentry.get()
    return steps

def dataperstepnumber():
    global datapstep
    datapstep = dataentry.get()
    return datapstep

def done():
    main_win.destroy()

#Labels
Label (main_win, text='How many cycles').grid(row=1, column=0)
Label (main_win, text='How many Vg sweep steps').grid(row=2, column=0)
Label (main_win, text='How many datapoints per step').grid(row=3, column=0)
Label (main_win, text='1- UPLOAD RunMe.ino to the Arduino board').grid(row=5,column=0)
Label (main_win, text='2- Run ardtoCsv.py for data acquisition').grid(row=6,column=0)
Label (main_win, text='3- mod.py for data treatment').grid(row=7,column=0)

#Text entries
cyclesentry= Entry(main_win, width=5)
cyclesentry.grid(row=1,column=1)

stepsentry=Entry(main_win,width=5)
stepsentry.grid(row=2, column=1)

dataentry=Entry(main_win, width=5)
dataentry.grid(row=3,column=1)

# buttons
button_cycles=Button(main_win, text='Submit', width= 10, command=cyclesnumber).grid(row=1, column=2)
button_steps=Button(main_win, text='Submit', width= 10, command=stepsnumber).grid(row=2, column=2)
button_data=Button(main_win, text='Submit', width=10, command=dataperstepnumber).grid(row=3, column=2)
button_done=Button(main_win,text='Generate Arduino file',width=30, command=done).grid(row=4,column=0)

main_win.mainloop()

cyclesStr = str("z<"+cycles)
stepsStr= str("i<"+steps)
dataStr=str("x<"+datapstep)



with open("copy.ino", "r") as f,\
     open(os.getcwd()+"\\RunMe\\RunMe.ino", "w") as outfile:
    lines=f.read()

    
    lines=lines.replace("z<NC",cyclesStr)
    lines=lines.replace("i<NS",stepsStr)
    lines=lines.replace("x<NDS",dataStr)
    
    outfile.write(lines)

