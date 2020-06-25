from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition

class GUIEvent(GUILinkable):
    
    PERIMETER = 60

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # Extract info
        eventtype = EventType.IntermediateThrow
        # cast
        cnv: Canvas = self.canvas
        # figure out the border width of the circle
        borderwidth = (4 if eventtype == EventType.End else 2)
        # draw borders
        self.id.append (cnv.create_oval(x, y, x + self.PERIMETER, y + self.PERIMETER, fill=cnv['bg'], outline=black, width=borderwidth))
        # draw inner border
        if eventtype in [EventType.IntermediateCatch, EventType.IntermediateThrow]:
            self.id.append (cnv.create_oval(x + 4, y + 4, x + self.PERIMETER - 4, y + self.PERIMETER - 4, fill=cnv['bg'], outline=black, width=borderwidth))
            

    def move(self, x, y):
        super().move(x - (self.PERIMETER/2), y - (self.PERIMETER/2))