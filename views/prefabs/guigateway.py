from tkinter import Canvas
from PIL import Image as Img, ImageTk as ImgTk
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable
from models.bpmn.enums.gatewaytype import GatewayType

class GUIGateway(GUILinkable):

    WIDTH = 60
    ICON_SIZE = 40

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # get information
        _type = GatewayType.ParallelEventBased
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

    def move(self, x, y):
        super().move(x - (self.WIDTH/2), y - (self.WIDTH/2))