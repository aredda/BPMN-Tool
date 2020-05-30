from tkinter import *
from helpers.colorhelper import *
from views.effects.animatable import Animatable
from resources.colors import *
from PIL import Image as Img, ImageTk

class IconFrame(Canvas, Animatable):

    def __init__(self, master, imagePath, imagePadding=15, bgColor=None, size=50, command=None, hoverBgColor=None, **args):
        Canvas.__init__(self, master, **args)
        Animatable.__init__(self)

        self.size = size
        self.imagePath = imagePath
        self.defaultBgColor = bgColor
        self.hoverBgColor = hoverBgColor
        # Remove border
        self.configure(highlightthickness=0)
        # Configure background colors
        self['bg'] = master['bg']
        self.bgColor = self['bg'] if bgColor is None else bgColor
        # Configure the size
        self.configure(width=size, height=size)
        # Draw rounded background
        self.bg_circle = self.create_oval(2, 2, size - 2, size - 2, fill=self.bgColor, width=0)
        # Configure image & draw image
        self._image = ImageTk.PhotoImage(Img.open(imagePath).resize((size-imagePadding, size-imagePadding)))
        self.image = self.create_image(size/2, size/2, image=self._image)
        # Configure click
        if command != None:
            self.bind('<Button-1>', command)

    def set_bgColor(self, color):
        self.bgColor = color
        self.itemconfig(self.bg_circle, fill=color)

    def get_bgColor(self):
        return self.bgColor

    ###
    ### Animation Section
    ###

    def onEnter(self):
        if self.hoverBgColor == None:
            return

        self.set_bgColor(self.hoverBgColor)

    def onLeave(self):
        if self.hoverBgColor == None:
            return

        self.set_bgColor(self.defaultBgColor)
        
