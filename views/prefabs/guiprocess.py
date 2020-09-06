from tkinter import Canvas
from resources.colors import *
from views.prefabs.abstract.guicontainer import GUIContainer
from views.prefabs.guilane import GUILane
from models.bpmn.lane import Lane
from models.bpmn.process import Process
from models.bpmndi.shape import BPMNShape
from models.bpmndi.bounds import Bounds

class GUIProcess(GUIContainer):

    WIDTH = 600
    HEIGHT = 400

    POST_OFFSET = 40
    TEXT_OFFSET = 16

    def __init__(self, **args):
        GUIContainer.__init__(self, **args)

        self.element = args.get('element', Process())
        self.dielement = args.get('dielement', BPMNShape())

        if self.dielement != None:
            self.dielement.isHorizontal = True

            if self.element != None:
                self.dielement.element = self.element

            if self.dielement.bounds == None:
                self.dielement.bounds = Bounds()

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
        cnv: Canvas = self.getcanvas()
        # draw process borders
        self.id.append (cnv.create_rectangle(x, y, x + self.WIDTH, y + self.HEIGHT, fill=cnv['bg'], outline=black, width=2))
        # vertical border
        vBorder = cnv.create_line(x + self.POST_OFFSET, y, x + self.POST_OFFSET, y + self.HEIGHT, fill=black, width=2)
        self.id.append (vBorder)
        # mark the vertical border as unselected element
        self.unselected.append (vBorder)
        # update di props
        self.update_diprops()

    def set_text(self, text):
        self.element.name = text
        # draw name of element
        self.draw_text(self.element.name, self.x + self.POST_OFFSET + self.WIDTH / 2, self.y - self.TEXT_OFFSET, self.WIDTH)

    def draw_lanes(self):
        # re-devide height
        correct_height = int (self.HEIGHT / len (self.lanes)) if self.lanes != [] else 0
        # proceed
        for lane in self.lanes:
            # erase
            lane.erase()
            # adjust height
            lane.HEIGHT, lane.WIDTH = correct_height, self.WIDTH
            # adjust where the lane is created
            yCorrect = self.y
            for l in self.lanes:
                if l == lane: break
                yCorrect += lane.HEIGHT
            # refresh
            lane.draw_at(self.x + self.POST_OFFSET, yCorrect)

    def add_lane(self, lane_model=None, autoFix=True):
        # create an empty lane
        lane = GUILane(width=self.WIDTH-self.POST_OFFSET, canvas=self.canvas, guiprocess=self, element=lane_model)
        lane.parent = self
        # append it to
        self.append_child(lane)
        self.lanes.append(lane)
        # can't possibly add one lane
        if autoFix:
            if len (self.lanes) == 1:
                extra_lane = GUILane(width=self.WIDTH-self.POST_OFFSET, canvas=self.canvas, guiprocess=self)
                self.append_child(extra_lane)
                self.lanes.append(extra_lane)
        # draw 
        self.draw_lanes()

    def remove_lane(self, lane, autoFix=True):
        # remove from containers
        lane.erase()
        self.lanes.remove(lane)
        self.remove_child(lane)
        # if there's only one lane left.. just delete it
        if autoFix and len(self.lanes) == 1:
            last_lane = self.lanes.pop()
            last_lane.erase()
            self.remove_child(last_lane)
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
        return [] if len (self.children) > len (self.lanes) else [{
            'text': 'Add Lane',
            'icon': 'add.png',
            'cmnd': lambda e: self.add_lane()
        }]
    
    def memento_setup(self):
        super().memento_setup()
        # revoke canvas
        self.canvas = None
        # lanes
        for lane in self.lanes: 
            lane.memento_setup()
