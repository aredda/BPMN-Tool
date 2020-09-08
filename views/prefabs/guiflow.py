from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guilinkable import Prefab, GUILinkable
from models.bpmn.sequenceflow import SequenceFlow, Flow
from models.bpmn.messageflow import MessageFlow
from models.bpmn.dataassociation import DataAssociation, Association
from models.bpmndi.edge import BPMNEdge

class GUIFlow(Prefab):

    SELECT_COLOR = teal
    DESELECT_COLOR = black
    TEXT_OFFSET = 16

    def __init__(self, **args):
        super().__init__(**args)

        self.guisource: Prefab = args.get('guisource', None)
        self.guitarget: Prefab = args.get('guitarget', None)
        
        self.dielement = args.get('dielement', BPMNEdge())

        # finish set up
        if self.guisource != None:
            self.guisource.add_flow(self)
        if self.guitarget != None:
            self.guitarget.add_flow(self)

    def draw_at(self, x, y):
        super().draw_at(x, y)
        cnv: Canvas = self.getcanvas()
        # figure out which ports to use
        sourceport = self.guisource.get_port_to(self.guitarget)
        targetport = self.guitarget.get_port_to(self.guisource)
        # find the text position
        ts = [
            (targetport[1][0] - sourceport[1][0]) / 2,
            (targetport[1][1] - sourceport[1][1]) / 2
        ]
        direction = [
            1 if ts[0] > 0 else -1,
            1 if ts[1] > 0 else -1
        ]
        text_pos = [
            sourceport[1][0] + direction[0] * abs(ts[0]),
            sourceport[1][1] + direction[1] * abs(ts[1])
        ]
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
        # draw text
        self.draw_text(self.element.name, int(text_pos[0]), int(text_pos[1]), 50)
        # update di props
        self.update_diprops()

    def destroy(self):
        # removing from models
        if isinstance(self.element, DataAssociation) == True:
            linkable = self.guisource.element if isinstance (self.guisource, GUILinkable) == True else self.guitarget.element 
            linkable.remove_data_link(self.element)
        elif isinstance(self.element, SequenceFlow) == True:
            self.element.separate()
        # destroy anyway
        super().destroy()

    def unlink(self):
        # remove from gui elements
        self.guisource.flows.remove(self)
        self.guitarget.flows.remove(self)

    def update_diprops(self):
        self.dielement.element = self.element
        self.dielement.start = self.guisource.get_port_to(self.guitarget) [1]
        self.dielement.end = self.guitarget.get_port_to(self.guisource) [1]