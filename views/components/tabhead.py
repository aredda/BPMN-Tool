from tkinter import *
from ui.colors import *
from ui.iconbutton import IconButton
from effects.color_transition import ColorTransition
from effects.animatable import Animatable

class TabHead(Frame, Animatable):

    def __init__(self, master, text: str, image: str, **args):
        Frame.__init__(self, master, **args)
        
        self.tag = args.get('tag', None)
        self.tabManager = args.get('manager', None)
        self.selected = False

        self.iconButton = IconButton(self, text, '-size 15', black, image, 25, None, black, bg=args['bg'])
        self.iconButton.pack (side=TOP)

        self.border = Frame(self, bg=black, height=5)
        self.border.pack_propagate(0)
        self.border.pack (side=TOP, fill=X, pady=5)

        self.transitions = []

        self.iconButton.bind_click(lambda e: self.on_click())

    def decorize(self, color):
        # Stop all transitions
        self.stop_transitions()
        self.clear()
        # Setters
        def setFntClr(v): self.iconButton.label['fg'] = v
        def setBrdrClr(v): self.border['bg'] = v
        def setImgBg(v): self.iconButton.icon.set_bgColor(v)
        # Getters
        getFntClr = lambda: self.iconButton.label['fg']
        getBrdrClr = lambda: self.border['bg']
        getImgBg = lambda: self.iconButton.icon.get_bgColor()
        # Change color
        self.save_transition( ColorTransition(setFntClr, getFntClr, color) )
        self.save_transition( ColorTransition(setBrdrClr, getBrdrClr, color) )
        self.save_transition( ColorTransition(setImgBg, getImgBg, color) )

    def on_click(self):
        if self.selected == False:
            self.tabManager.select_tab(self.tag)

    def select(self):
        self.selected = True
        self.decorize (teal)

    def deselect(self):
        self.selected = False
        self.decorize (black)