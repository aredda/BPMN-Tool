from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable

class GUIGateway(GUILinkable):

    WIDTH = 60

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        # get canvas
        cnv: Canvas = self.canvas
        # draw border
        cnv.create_polygon(
            x + self.WIDTH/2, y,
            x + self.WIDTH, y + self.WIDTH/2,
            x + self.WIDTH/2, y + self.WIDTH,
            x, y + self.WIDTH/2,
            fill=cnv['bg'], outline=black, width=2
        )
