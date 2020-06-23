from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import GUILinkable

class GUIActivity(GUILinkable):
    
    WIDTH = 150
    HEIGHT = 100
    RADIUS = 10

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        # get canvas
        cnv: Canvas = self.canvas
        # border points
        points = [
            x+self.RADIUS, y,
            x+self.RADIUS, y,
            x + self.WIDTH-self.RADIUS, y,
            x + self.WIDTH-self.RADIUS, y,
            x + self.WIDTH, y,
            x + self.WIDTH, y+self.RADIUS,
            x + self.WIDTH, y+self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT-self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT-self.RADIUS,
            x + self.WIDTH, y + self.HEIGHT,
            x + self.WIDTH-self.RADIUS, y + self.HEIGHT,
            x + self.WIDTH-self.RADIUS, y + self.HEIGHT,
            x+self.RADIUS, y + self.HEIGHT,
            x+self.RADIUS, y + self.HEIGHT,
            x, y + self.HEIGHT,
            x, y + self.HEIGHT-self.RADIUS,
            x, y + self.HEIGHT-self.RADIUS,
            x, y+self.RADIUS,
            x, y+self.RADIUS,
            x, y
        ]
        # draw border
        cnv.create_polygon(points, fill=cnv['bg'], width=2, outline=black, smooth=True)
