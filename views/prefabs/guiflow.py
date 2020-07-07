from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.prefab import Prefab
from models.bpmn.sequenceflow import SequenceFlow
from models.bpmn.messageflow import MessageFlow
from models.bpmn.association import Association

class GUIFlow(Prefab):

    def __init__(self, **args):
        super().__init__(**args)

        self.guisource: Prefab = args.get('guisource', None)
        self.guitarget: Prefab = args.get('guitarget', None)

        # finish set up
        if self.guisource != None:
            self.guisource.add_flow(self)
        if self.guitarget != None:
            self.guitarget.add_flow(self)

    def draw_at(self, x, y):
        super().draw_at(x, y)

        cnv: Canvas = self.canvas
        # figure out which ports to use
        sourceport = self.guisource.get_port_to(self.guitarget)
        targetport = self.guitarget.get_port_to(self.guisource)
        # draw line
        self.id.append (cnv.create_line(sourceport, targetport, width=2, fill=black))
