from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition

class GUIEvent(GUILinkable):
    
    PERIMETER = 60
    ICON_SIZE = 36
    LABEL_OFFSET = 16

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

        self.WIDTH = self.HEIGHT = self.PERIMETER

        self.temp_type = EventType.Start
        self.temp_def = EventDefinition.Cancel
        self.temp_text = 'Event Name'

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # Extract info
        eventtype = self.temp_type
        eventdefinition = self.temp_def
        text = self.temp_text
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
            if eventtype in [EventType.End, EventType.IntermediateThrow] and eventdefinition != EventDefinition.Message:
                overlaid_img = Img.new('RGBA', image.size, color=black)
                overlaid_img.putalpha(image.getchannel('A'))
                self.def_icon = ImgTk.PhotoImage(overlaid_img)
            self.id.append (cnv.create_image(x + self.PERIMETER/2, y + self.PERIMETER/2, image=self.def_icon))
        # draw event's name
        self.draw_text(text, x + self.PERIMETER/2, y - self.LABEL_OFFSET)

    def get_options(self):
        option_list = []

        def mediator(t, d):
            return lambda e: self.configure(t, d)

        for t in list(EventType):
            tstr = str(t).split('.')[1]
            option_list.append({
                'folder': 'resources/icons/notation/',
                'icon': (tstr.lower() if t in [EventType.Start, EventType.End] else 'intermediate') + 'event.png',
                'text': f'Change to {tstr} Event',
                'fg': silver,
                'textfg': gray,
                'cmnd': mediator(t, self.temp_def)
            })

        for d in list(EventDefinition):
            dstr = str(d).split('.')[1]
            # adjust path
            path = dstr.lower()
            etype = EventType.End
            if d == EventDefinition.Message: path = 'receive' if etype not in [EventType.Start, EventType.IntermediateThrow] else 'send'
            # add option item
            option_list.append({
                'folder': 'resources/icons/notation/',
                'icon': (path if d != EventDefinition.Default else 'startevent') + '.png',
                'text': f'Define as {dstr}',
                'fg': gray2,
                'textfg': gray,
                'cmnd': mediator(self.temp_type, d)
            })

        return option_list

    def configure(self, etype, edefinition):
        self.temp_type = etype
        self.temp_def = edefinition
        self.destroy()
        self.draw()