from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable

class GUIGateway(GUILinkable):

    WIDTH = 60

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
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

    def move(self, x, y):
        super().move(x - (self.WIDTH/2), y - (self.WIDTH/2))