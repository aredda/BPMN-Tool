from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guicontainer import GUIContainer
from views.prefabs.abstract.guilinkable import GUILinkable

class GUIProcess(GUILinkable):

    WIDTH = 600
    HEIGHT = 400

    def __init__(self, **args):
        GUILinkable.__init__(self, **args)

    def draw_at(self, x, y):
        GUILinkable.draw_at(self, x, y)
        # retrieve canvas
        cnv: Canvas = self.canvas
        # draw process borders
        self.id.append (cnv.create_rectangle(x, y, x + self.WIDTH, y + self.HEIGHT, fill=cnv['bg'], outline=black, width=2))
        # horizontal border
        self.id.append (cnv.create_line(x + 40, y, x + 40, y + self.HEIGHT, fill=black, width=2))

    def move(self, x, y):
        super().move(x - (self.WIDTH/2), y - (self.HEIGHT/2))