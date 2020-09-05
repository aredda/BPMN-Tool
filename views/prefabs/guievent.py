from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from helpers.cachemanager import CacheManager
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.event import Event, EventType, EventDefinition
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIEvent(GUILinkable):
    
    PERIMETER = 60
    ICON_SIZE = 36
    LABEL_OFFSET = 16

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

        self.element = args.get('element', Event())
        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement.bounds == None:
            self.dielement.bounds = Bounds()

        # adjust dimensions
        self.WIDTH = self.HEIGHT = self.PERIMETER
        # ban these props when serializing memento
        self.memento_banlist.append('def_icon')

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # Extract info
        eventtype = self.element.type
        eventdefinition = self.element.definition
        text = self.element.name
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
            cachekey = 'img_' + str(self.element.definition) + '_' + str(self.element.type) + '_' + str(self.ICON_SIZE)
            self.def_icon = CacheManager.get_cached_image(cachekey)
            if self.def_icon == None:
                image = Img.open(folder + pure_name + '.png').resize((self.ICON_SIZE, self.ICON_SIZE))
                # cache for better performance
                self.def_icon = CacheManager.get_or_add_if_absent(cachekey, ImgTk.PhotoImage(image))
                # add a black overlay if it's end/throw event
                if eventtype in [EventType.End, EventType.IntermediateThrow] and eventdefinition != EventDefinition.Message:
                    overlaid_img = Img.new('RGBA', image.size, color=black)
                    overlaid_img.putalpha(image.getchannel('A'))
                    self.def_icon = ImgTk.PhotoImage(overlaid_img)
                    # update cache
                    CacheManager.add_cache_record(cachekey, self.def_icon)
            self.id.append (cnv.create_image(x + self.PERIMETER/2, y + self.PERIMETER/2, image=self.def_icon))
        # draw event's name
        self.draw_text(text, x + self.PERIMETER/2, y - self.LABEL_OFFSET)

    def get_options(self):
        option_list = []

        def mediator(t, d):
            return lambda e: self.configure(t, d)

        # change type options
        for t in list(EventType):
            # skip activated options
            if t == self.element.type: continue
            # proceed
            tstr = str(t).split('.')[1]
            option_list.append({
                'folder': 'resources/icons/notation/',
                'icon': (tstr.lower() if t in [EventType.Start, EventType.End] else 'intermediate') + 'event.png',
                'text': f'Change to {tstr} Event',
                'fg': silver,
                'textfg': gray,
                'cmnd': mediator(t, None)
            })

        # change definition options
        for d in list(EventDefinition):
            # skip current option
            if d == self.element.definition: continue
            # proceed
            dstr = str(d).split('.')[1]
            # adjust path
            path = dstr.lower()
            if d == EventDefinition.Message: path = 'receive' if self.element.type not in [EventType.Start, EventType.IntermediateThrow] else 'send'
            # add option item
            option_list.append({
                'folder': 'resources/icons/notation/',
                'icon': (path if d != EventDefinition.Default else 'startevent') + '.png',
                'text': f'Define as {dstr}',
                'fg': gray2,
                'textfg': gray,
                'cmnd': mediator(None, d)
            })

        return option_list

    def configure(self, etype, edefinition):
        self.element.type = etype if etype != None else self.element.type
        self.element.definition = edefinition if edefinition != None else self.element.definition
        self.erase()
        self.draw()

    def scale(self, factor):
        if factor < 0 and (self.PERIMETER <= abs(factor) or self.ICON_SIZE <= abs(factor)):
            return
        # change values
        self.PERIMETER += factor
        self.ICON_SIZE += factor
        # redraw
        super().scale(factor)
    
    def resize(self, w, h):
        super().resize(w, h)
        # update di props
        self.update_diprops()

    def move(self, x, y):
        super().move(x, y)
        # update di props
        self.update_diprops()