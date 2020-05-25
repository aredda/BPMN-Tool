from views.resources.colors import *
from views.components.iconbutton import IconButton

def MainButton(master, text, iconPath, btnCmd = None):
    return IconButton(master, text, '-size 12 -weight bold', teal, iconPath, 12, {'bg': teal, 'fg': '#ffffff'}, teal, 40, btnCmd, highlightbackground=border, highlightthickness=1, padx=5, pady=5, bg='#ffffff')

def SecondaryButton(master, text, iconPath, btnCmd = None):
    return IconButton(master, text, '-size 12 -weight bold', white, iconPath, 12, {'fg': teal, 'bg': white, 'config': {'highlightbackground':border, 'highlightthickness':1}}, teal, 40, btnCmd, padx=5, pady=5, bg=teal)