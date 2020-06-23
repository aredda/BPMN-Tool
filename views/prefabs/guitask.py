from tkinter import Canvas
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity

class GUITask(GUIActivity):
    
    def __init__(self, **args):
        GUIActivity.__init__(self, **args)

    def draw_at(self, x, y):
        pass
