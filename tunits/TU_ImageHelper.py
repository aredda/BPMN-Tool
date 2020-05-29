from helpers.imagehelper import *
from tkinter import *
from views.components.icon import IconFrame

def run():
    p = 'resources/icons/notation/'
    path = svg_to_png(p + 'connection-multi.svg', 'resources/icons/temp/temp.png')

    win = Tk()
    ic = IconFrame(win, path)
    ic.pack()

    win.mainloop()