from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition

class GUIEvent(GUILinkable):
    
    PERIMETER = 60
    ICON_SIZE = 40

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # Extract info
        eventtype = EventType.End
        eventdefinition = EventDefinition.Terminate
        # cast
        cnv: Canvas = self.canvas
        # figure out the border width of the circle
        borderwidth = (6 if eventtype == EventType.End else 2)
        # draw borders
        self.id.append (cnv.create_oval(x, y, x + self.PERIMETER, y + self.PERIMETER, fill=cnv['bg'], outline=black, width=borderwidth))
        # draw inner border
        if eventtype in [EventType.IntermediateCatch, EventType.IntermediateThrow]:
            self.id.append (cnv.create_oval(x + 4, y + 4, x + self.PERIMETER - 4, y + self.PERIMETER - 4, fill=cnv['bg'], outline=black, width=borderwidth))
        # draw definition icon
        if eventdefinition != EventDefinition.Default:
            folder = 'resources/icons/notation/'
            pure_name = str(eventdefinition).split('.')[1].lower()
            # correct names
            if eventdefinition == EventDefinition.Message:
                pure_name = 'receive' if eventtype not in [EventType.Start, EventType.IntermediateThrow] else 'send'
            # display icon
            image = Img.open(folder + pure_name + '.png').resize((self.ICON_SIZE, self.ICON_SIZE))
            self.def_icon = ImgTk.PhotoImage(image)
            # add a black overlay if it's end/throw event
            if eventtype in [EventType.End, EventType.IntermediateThrow]:
                overlaid_img = Img.new('RGBA', image.size, color=black)
                overlaid_img.putalpha(image.getchannel('A'))
                self.def_icon = ImgTk.PhotoImage(overlaid_img)
            self.id.append (cnv.create_image(self.PERIMETER/2, self.PERIMETER/2, image=self.def_icon))
            
    def move(self, x, y):
        super().move(x - (self.PERIMETER/2), y - (self.PERIMETER/2))