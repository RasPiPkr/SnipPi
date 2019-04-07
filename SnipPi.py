#! /usr/bin/python3
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as font
from tkinter import *
import subprocess, time, os
from PIL import Image

# Capture as a temp_file for processing.
temp_file = 'SnipPi_Preview_Close_Me.png'

# SnipPi usage information.
mouse = 'After clicking "Take SnipPi" using left mouse button and hold it down and drag over your desired area, when you release the mouse button that area will be captured.'
window = 'After clicking "Take SnipPi" you then click on the window to capture, make sure your window is not minimised as your next mouse click will be the selection.'
fullscreen = 'After clicking "Take SnipPi" a full screenshot will be taken without the mouse pointer. Everything on your screen will be included.'

root = Tk()
root.title('SnipPi')
font.nametofont('TkDefaultFont').configure(size=12)
root.geometry('585x155')
root.resizable(0, 0)

selected = IntVar()
selected.set(1)
textStr = StringVar()
textStr.set(mouse)

def showInfo():
    showText = selected.get()
    if showText == 1:
        textStr.set(mouse)
    elif showText == 2:
        textStr.set(window)
    elif showText == 3:
        textStr.set(fullscreen)

def snipHandler():
    root.iconify()
    snipPit = selected.get()
    if snipPit == 1:
        sel_win()
    elif snipPit == 2:
        sel_win()
    elif snipPit == 3:
        time.sleep(1)
        full_scrn()

def sel_win():
    subprocess.call('sudo scrot -s {}'.format(temp_file), shell=True)
    showSave()

def full_scrn():
    subprocess.call('sudo scrot {}'.format(temp_file), shell=True)
    showSave()

def showSave():
    os.system('xdg-open {}'.format(temp_file))
    time.sleep(2)
    save_as = filedialog.asksaveasfile(mode='w',
                                       parent=root,
                                       initialdir='/home/pi/',
                                       title = 'Save SnipPi',
                                       filetypes=(("PNG","*.png"),("JPG","*.jpg")))
    if not save_as:
        subprocess.call('sudo rm {}'.format(temp_file), shell=True) # temp file now deleted.
        messagebox.showinfo('SnipPi', 'Save cancelled by user, please close preview window.')
    else:
        img = Image.open(temp_file)
        img.save(save_as.name)
        subprocess.call('sudo rm {}'.format(temp_file), shell=True) # temp file now deleted.

Label(root, text='Please select from the following:').grid(row=0, column=0, columnspan=4, padx=5, pady=5)
Radiobutton(root, text='User ', width=10, variable=selected, value=1, command=showInfo).grid(row=1, column=0, padx=5, pady=5)
Radiobutton(root, text='Window', width=10, variable=selected, value=2, command=showInfo).grid(row=1, column=1, padx=5, pady=5)
Radiobutton(root, text='Full Screen',width=10,  variable=selected, value=3, command=showInfo).grid(row=1, column=2, padx=5, pady=5)
Button(root, text='Take SnipPi', width=10, fg='red', command=snipHandler).grid(row=1, column=3, padx=5, pady=5)
Label(root, textvariable=textStr, wraplength=500).grid(row=2, columnspan=4, padx=5, pady=5)

root.mainloop()
