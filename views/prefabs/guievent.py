from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.eventtype import EventType

class GUIEvent(GUILinkable):
    
    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        # cast
        cnv: Canvas = self.canvas
        # draw borders
        cnv.create_oval(x, y, x + 75, y + 75, fill=white)
        
        