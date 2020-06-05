from tkinter import *
from resources.colors import *
from views.components.iconbutton import IconButton
from views.effects.color_transition import ColorTransition
from views.effects.animatable import Animatable

class TabHead(Frame, Animatable):

    def __init__(self, master, text: str, image: str, **args):
        Frame.__init__(self, master, **args)
        
        self.tag = args.get('tag', None)
        self.tabManager = args.get('manager', None)
        self.selected = False

        self.iconButton = IconButton(self, text, '-size 18', black, image, 23, None, black, bg=args.get('bg', background))
        self.iconButton.label.pack (side=LEFT, padx=(10, 0))
        self.iconButton.pack (side=TOP, anchor='nw')

        self.border = Frame(self, bg=black, height=5)
        self.border.pack_propagate(0)
        self.border.pack (side=BOTTOM, fill=X, pady=5)

        self.transitions = []

        self.iconButton.bind_click(lambda e: self.on_click())

    def decorize(self, color):
        # Stop all transitions
        self.stop_transitions()
        self.clear()
        # Setters
        def setFntClr(v): self.iconButton.label['fg'] = v
        def setBrdrClr(v): self.border['bg'] = v
        # Getters
        getFntClr = lambda: self.iconButton.label['fg']
        getBrdrClr = lambda: self.border['bg']
        # Change color
        self.save_transition( ColorTransition(setFntClr, getFntClr, color) )
        self.save_transition( ColorTransition(setBrdrClr, getBrdrClr, color) )
        self.iconButton.icon.set_bgColor(color)

    def on_click(self):
        if self.selected == False:
            self.tabManager.select_tab(self.tag)

    def select(self):
        self.selected = True
        self.decorize (teal)

    def deselect(self):
        self.selected = False
        self.decorize (black)