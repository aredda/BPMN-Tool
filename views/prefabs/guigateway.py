from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from helpers.cachemanager import CacheManager
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.gateway import Gateway, GatewayType
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIGateway(GUILinkable):

    ICON_SIZE = 34
    LABEL_OFFSET = 16

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

        self.element = args.get('element', Gateway())
        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement != None:
            if self.dielement.bounds == None:
                self.dielement.bounds = Bounds()

        # set up dimensions
        self.WIDTH = self.HEIGHT = 60
        # pre memento serialization
        self.memento_banlist = ['type_icon']

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # get information
        _type = self.element.type
        # get canvas
        cnv: Canvas = self.getcanvas()
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
            cachekey = 'gt_img_' + str(self.element.type) + '_' + str(self.ICON_SIZE)
            # attempt to retrieve a cached image
            self.type_icon = CacheManager.get_cached_image(cachekey) 
            if self.type_icon == None:
                # cache image if not cached
                folder = 'resources/icons/notation/'
                filename = str(_type).split('.')[1].lower()
                self.type_icon = CacheManager.get_or_add_if_absent (cachekey, ImgTk.PhotoImage(Img.open(folder + filename + '.png').resize((self.ICON_SIZE, self.ICON_SIZE))))
            self.id.append (cnv.create_image(x + self.WIDTH/2, y + self.WIDTH/2, image=self.type_icon))
        # Draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y - self.LABEL_OFFSET)

    def get_options(self):
        olist = []

        def corrector(t):
            return lambda e: self.configure(t)

        for t in list(GatewayType):
            # skip current type
            if self.element.type == t: continue
            # proceed
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

    def scale(self, factor):
        # change icon size
        self.ICON_SIZE += factor
        # call the super scale
        super().scale(factor)