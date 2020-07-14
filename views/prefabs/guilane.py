from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guicontainer import GUIContainer

class GUILane(GUIContainer):

    def __init__(self, **args):
        GUIContainer.__init__(self, **args)

        self.guiprocess = args.get('guiprocess', None)
        self.WIDTH = args.get('width', 0)
        self.HEIGHT = args.get('height', 100)

    def draw_at(self, x, y):
        super().draw_at(x, y)
        # retrieve canvas
        cnv: Canvas = self.canvas
        # draw lane
        self.id.append(cnv.create_rectangle(x, y, x + self.WIDTH, y + self.HEIGHT, fill=background, width=2, outline=black))
        # refresh children
        for c in self.children:
            c.erase()
            c.draw()

    def append_child(self, child):
        if child.__class__.__name__ not in ['GUIProcess', 'GUILane']:
            super().append_child(child)

    def destroy(self):
        # remove from parent
        self.guiprocess.remove_lane(self)
        # remove self
        super().destroy()
        # clear
        self.children.clear()

    # disable resize func
    def resize(self, w, h): pass
    
        