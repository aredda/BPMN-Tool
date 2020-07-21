from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.gateway import Gateway, GatewayType
from models.bpmndi.shape import BPMNShape

class GUIGateway(GUILinkable):

    ICON_SIZE = 34
    LABEL_OFFSET = 16

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

        self.element = args.get('element', Gateway())
        self.dielement = args.get('dielement', BPMNShape())

        self.WIDTH = self.HEIGHT = 60

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # get information
        _type = self.element.type
        # get canvas
        cnv: Canvas = self.canvas
        # draw border
        self.id.append (cnv.create_polygon(
            x + self.WIDTH/2, y,
            x + self.WIDTH, y + self.WIDTH/2,
            x + self.WIDTH/2, y + self.WIDTH,
            x, y + self.WIDTH/2,
            fill=cnv['bg'], outline=black, width=2
        ))
        # draw icon
        if _type != GatewayType.Exclusive:
            folder = 'resources/icons/notation/'
            filename = str(_type).split('.')[1].lower()
            self.type_icon = ImgTk.PhotoImage(Img.open(folder + filename + '.png').resize((self.ICON_SIZE, self.ICON_SIZE)))
            self.id.append (cnv.create_image(x + self.WIDTH/2, y + self.WIDTH/2, image=self.type_icon))
        # Draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y - self.LABEL_OFFSET)

    def get_options(self):
        olist = []

        def corrector(t):
            return lambda e: self.configure(t)

        for t in list(GatewayType):
            tstr = str(t).split('.')[1]
            olist.append({
                'folder': 'resources/icons/notation/',
                'icon': ('gateway' if t == GatewayType.Exclusive else tstr.lower()) + '.png',
                'text': f'Change to {tstr} Gateway',
                'fg': gray2,
                'textfg': gray,
                'cmnd': corrector(t)
            })

        return olist

    def configure(self, t):
        self.element.type = t
        self.erase()
        self.draw()