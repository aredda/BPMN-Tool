from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guicontainer import GUIContainer
from views.prefabs.guilane import GUILane
from models.bpmn.process import Process
from models.bpmndi.plane import BPMNPlane

class GUIProcess(GUIContainer):

    WIDTH = 600
    HEIGHT = 400

    POST_OFFSET = 40

    def __init__(self, **args):
        GUIContainer.__init__(self, **args)

        self.element = args.get('element', Process())
        self.dielement = args.get('dielement', BPMNPlane())

        self.lanes = []

    def match(self, id):
        # match lanes too
        for lane in self.lanes:
            if lane.match(id) != None:
                return lane
        # otherwise continue
        return super().match(id)

    def draw_at(self, x, y):
        GUIContainer.draw_at(self, x, y)
        # retrieve canvas
        cnv: Canvas = self.canvas
        # draw process borders
        self.id.append (cnv.create_rectangle(x, y, x + self.WIDTH, y + self.HEIGHT, fill=cnv['bg'], outline=black, width=2))
        # horizontal border
        self.id.append (cnv.create_line(x + self.POST_OFFSET, y, x + self.POST_OFFSET, y + self.HEIGHT, fill=black, width=2))

    def draw_lanes(self):
        # re-devide height
        correct_height = int (self.HEIGHT / len (self.lanes)) if self.lanes != [] else 0
        # proceed
        for lane in self.lanes:
            # erase
            lane.erase()
            # adjust height
            lane.HEIGHT = correct_height
            # adjust where the lane is created
            yCorrect = self.y
            for l in self.lanes:
                if l == lane: break
                yCorrect += lane.HEIGHT
            # refresh
            lane.draw_at(self.x + self.POST_OFFSET, yCorrect)

    def add_lane(self):
        # create an empty lane
        lane = GUILane(width=self.WIDTH-self.POST_OFFSET, canvas=self.canvas, guiprocess=self)
        # append it to
        self.children.append(lane)
        self.lanes.append(lane)
        # can't possibly add one lane
        if len (self.lanes) == 1:
            extra_lane = GUILane(width=self.WIDTH-self.POST_OFFSET, canvas=self.canvas, guiprocess=self)
            self.children.append(extra_lane)
            self.lanes.append(extra_lane)
        # draw 
        self.draw_lanes()

    def remove_lane(self, lane):
        # remove from containers
        lane.erase()
        self.lanes.remove(lane)
        self.children.remove(lane)
        # if there's only one lane left.. just delete it
        if len(self.lanes) == 1:
            last_lane = self.lanes[0]
            last_lane.erase()
            self.children.remove(last_lane)
            self.lanes.clear()
        # redraw
        self.draw_lanes()

    def resize(self, width, height):
        super().resize(width, height)
        # update the width
        for lane in self.lanes:
            lane.WIDTH = width - self.POST_OFFSET
            lane.HEIGHT = height / len (self.lanes)
        # redraw lanes
        self.draw_lanes()

    def scale(self, factor):
        super().scale(factor)
        # refresh
        self.draw_lanes()

    def get_options(self):
        return [{
            'text': 'Add Lane',
            'icon': 'add.png',
            'cmnd': lambda e: self.add_lane()
        }]