from tkinter import *
from views.resources.colors import *
from views.components.tabhead import TabHead
from effects.move_transition import MoveTransition
from effects.animatable import Animatable

class TabManager(Frame, Animatable):

    def __init__(self, master, **args):
        Frame.__init__(self, master, **args)

        self.tabHeads = {}
        self.tabBodies = {}

        self.selectedHead = None
        self.selectedBody = None

        self.pack (fill=X)

        self.transitions = []

    def add_head (self, tag, head: TabHead):
        self.tabHeads[tag] = head
        head.tabManager = self
        head.tag = tag
        head.pack (side=LEFT, padx=15)

    def connect_body (self, tag, body):
        self.tabBodies[tag] = body
        body.pack_forget()

    def initialize(self):
        firstKey = list(self.tabHeads.keys())[0]
        # Decorate
        self.tabHeads[firstKey].select()
        self.tabBodies[firstKey].place(x=0, y=0, relwidth=1)
        # Change indicators
        self.selectedHead = firstKey
        self.selectedBody = self.tabBodies[firstKey]

    def select_tab(self, tag):
        # Turn off all tab heads
        for t in self.tabHeads.keys():
            self.tabHeads[t].deselect()
        # Turn on the clicked tab head
        self.tabHeads[tag].select()
        # Animate
        self.stop_transitions()
        self.clear ()

        diff = list (self.tabHeads.keys()).index(self.selectedHead) - list (self.tabHeads.keys()).index(tag)
        steadyPoint = -1024 if diff < 0 else 1024
        hidePoint = steadyPoint * -1
        self.tabBodies[tag].place(x=steadyPoint, y=0, relwidth=1)

        def get_set(body): return lambda v: body.place(x=v, y=0, relwidth=1)
        def get_get(body): return lambda: int (body.place_info()['x'])

        self.save_transition (MoveTransition(get_set(self.selectedBody), get_get(self.selectedBody), hidePoint, 2.5))
        self.save_transition (MoveTransition(get_set(self.tabBodies[tag]), get_get(self.tabBodies[tag]), 0, 2.5))
        # Change indicators
        self.selectedHead = tag
        self.selectedBody = self.tabBodies[tag]

