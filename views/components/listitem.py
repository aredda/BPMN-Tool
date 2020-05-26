from tkinter import *
from resources.colors import *
from views.components.icon import IconFrame
from views.components.iconbutton import IconButton

class ListItem(Frame):
    
    def __init__(self, master, dataObject, bindings, buttons, creationMethod = None, **args):
        Frame.__init__(self, master, **args)

        self.buttons = []

        self.dataObject = dataObject
        self.bindings = bindings
        self.buttonSettings = buttons
        self.creationMethod = creationMethod

        self.create()

    def create(self):
        self.configure(padx=10, pady=10, relief=SOLID, highlightthickness=1, highlightbackground=border, bg=white)

        self.img_icon = IconFrame(self, 'icons/2x/face.png', 15, black)
        self.img_icon.pack(side=LEFT)

        self.lbl_username = Label(self, text='Username', bg=white, font='-size 12 -weight bold', fg=black)
        self.lbl_username.pack(side=LEFT, fill=Y, padx=5)

        for s in self.buttonSettings:
            btn = IconButton(self, s.get('text', 'Button Text'), '-size 10 -weight bold', teal, s.get('icon', 'icons/2x/error.png'), 15, {'fg': white, 'bg': teal}, teal, 30, s.get('cmd', None), bg=white, highlightthickness=1, highlightbackground=border, padx=7, pady=5)
            btn.pack(side=RIGHT, padx=(0, 5))
            self.buttons.append(btn)

