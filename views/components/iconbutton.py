from tkinter import *
from views.resources.colors import *
from views.components.icon import IconFrame
from effects.animatable import Animatable
from effects.color_transition import ColorTransition

class IconButton(Frame, Animatable):

    def __init__(self, master, text, textFont, textColor, imagePath, imageScale, hoverEff: dict, imgBgColor=None, imgSize=50, btnCommand = None, **args):
        Frame.__init__(self, master, **args)
        Animatable.__init__(self)

        self.hover_theme = hoverEff
        # Create the icon
        self.icon = IconFrame(self, imagePath, imageScale, imgBgColor, imgSize)
        self.icon.pack (side=LEFT)
        # Create the label
        self.label = Label(self, text=text, font=textFont, fg=textColor, bg=self['bg'])
        self.label.pack (side=LEFT, padx=(2, 0))
        # Save the initial theme
        self.theme = {
            'bg': self['bg'],
            'fg': textColor
        }
        # Bind click event
        if btnCommand != None:
            self.bind_click(btnCommand)

    def bind_click (self, command):
        self.bind('<Button-1>', command)
        self.label.bind('<Button-1>', command)
        self.icon.bind('<Button-1>', command)

    def onEnter(self):
        if self.hover_theme == None:
            return

        Animatable.onEnter(self)

        def set1(v): self['bg'] = v 
        def set2(v): self.label['bg'] = v 
        def set3(v): self.icon['bg'] = v 
        def set4(v): self.label['fg'] = v

        get1 = lambda: self['bg'] 
        get2 = lambda: self.label['bg'] 
        get3 = lambda: self.icon['bg']
        get4 = lambda: self.label['fg']

        self.save_transition(ColorTransition(set1, get1, self.hover_theme['bg']))
        self.save_transition(ColorTransition(set2, get2, self.hover_theme['bg']))
        self.save_transition(ColorTransition(set3, get3, self.hover_theme['bg']))
        self.save_transition(ColorTransition(set4, get4, self.hover_theme['fg']))

        if 'config' in self.hover_theme:
            self.configure(**self.hover_theme['config'])

    def onLeave(self):
        if self.hover_theme == None:
            return

        self.temp_theme = self.hover_theme
        self.hover_theme = self.theme
        self.onEnter ()
        self.hover_theme = self.temp_theme

