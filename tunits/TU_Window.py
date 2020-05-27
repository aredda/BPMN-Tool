from views.windows.abstract.window import Window
from views.windows.abstract.sessionwindow import SessionWindow
from views.windows.abstract.tabbedwindow import TabbedWindow
from views.windows.homewindow import HomeWindow
from views.windows.projectwindow import ProjectWindow
from views.components.scrollableframe import Scrollable
from tkinter import *
from resources.colors import *

def run():
    # window = HomeWindow()
    window = ProjectWindow()

    window.mainloop()
