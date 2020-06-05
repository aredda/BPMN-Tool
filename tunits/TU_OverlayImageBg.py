from PIL import Image as Img, ImageTk
from tkinter import *

def run():

    win = Tk()

    # Open original image and extract the alpha channel
    im = Img.open('resources/icons/ui/info.png')
    alpha = im.getchannel('A')

    # Create red image the same size and copy alpha channel across
    red = Img.new('RGBA', im.size, color='#333')
    red.putalpha(alpha) 

    img = ImageTk.PhotoImage(red)

    lbl = Label(win, image=img)
    lbl.pack()

    win.mainloop()
