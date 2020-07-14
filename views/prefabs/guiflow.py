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

        print (type(self.element))

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
        # draw the pointing arrow
        points = []
        for i in range(0, 3): points.append(list(targetport[1]))
        # correct
        vTargetPort = list(targetport[1])
        edge = 7
        longEdge = 10
        if targetport[0] in [self.LEFT_PORT, self.RIGHT_PORT]:
            xPrev = points[0][0]
            points[0][0] = points[2][0] = xPrev + longEdge * (1 if targetport[0] == self.RIGHT_PORT else -1)
            points[0][1] -= edge
            points[2][1] += edge
            vTargetPort[0] += longEdge * (1 if targetport[0] == self.RIGHT_PORT else -1) 
        if targetport[0] in [self.TOP_PORT, self.BOTTOM_PORT]:
            yPrev = points[0][1]
            points[0][1] = points[2][1] = yPrev + longEdge * (1 if targetport[0] == self.BOTTOM_PORT else -1)
            points[0][0] -= edge
            points[2][0] += edge
            vTargetPort[1] += longEdge * (1 if targetport[0] == self.BOTTOM_PORT else -1)
        # line options
        lineOpts = {
            'width': 2,
            'fill': black
        }
        if isinstance(self.element, SequenceFlow) == False:
            lineOpts['dash'] = (20, 10) if isinstance(self.element, MessageFlow) == True else (1, 10)
        # draw line
        self.id.append(cnv.create_line(sourceport[1], vTargetPort, **lineOpts))
        # draw arrow
        self.id.append(cnv.create_polygon(points, fill=black))
