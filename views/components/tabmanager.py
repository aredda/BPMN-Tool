from tkinter import *
from resources.colors import *
from views.components.tabhead import TabHead
from views.effects.move_transition import MoveTransition
from views.effects.animatable import Animatable

class TabManager(Frame, Animatable):

    def __init__(self, master, **args):
        Frame.__init__(self, master, **args)

        self.parent = master

        self.tabHeads = {}
        self.tabBodies = {}

        self.selectedHead = None
        self.selectedBody = None

        self.pack (fill=X)

        self.transitions = []

    def add_head (self, tag, head: TabHead):
        head.tabManager = self
        head.tag = tag
        head.pack (side=LEFT, padx=(0 if len (self.tabHeads) == 0 else 20, 0), fill=X, expand=1)
        # Save item
        self.tabHeads[tag] = head

    def connect_body (self, tag, body):
        self.tabBodies[tag] = body
        body.pack_forget()

    def initialize(self):
        firstKey = list(self.tabHeads.keys())[0]
        # Decorate
        self.tabHeads[firstKey].select()
        self.tabBodies[firstKey].place(x=0, y=0, relwidth=1, relheight=1)
        # Change indicators
        self.selectedHead = firstKey
        self.selectedBody = self.tabBodies[firstKey]

    def select_tab(self, tag):
        # Turn off all tab heads
        for t in self.tabHeads.keys():
            self.tabHeads[t].deselect()
        # Animate
        self.stop_transitions()
        self.clear ()
        # Turn on the clicked tab head
        self.tabHeads[tag].select()
        # Check if tag exists
        if tag not in self.tabBodies:
            return
        # Animation
        diff = list (self.tabHeads.keys()).index(self.selectedHead) - list (self.tabHeads.keys()).index(tag)
        steadyPoint = self.parent.winfo_width()
        steadyPoint = steadyPoint if diff < 0 else -steadyPoint
        hidePoint = steadyPoint * -1
        
        self.tabBodies[tag].place(x=steadyPoint, y=0, relwidth=1, relheight=1)

        def get_set(body): return lambda v: body.place(x=v, y=0, relwidth=1, relheight=1)
        def get_get(body): return lambda: int (body.place_info()['x'])

        self.save_transition (MoveTransition(get_set(self.selectedBody), get_get(self.selectedBody), hidePoint, 2.5))
        self.save_transition (MoveTransition(get_set(self.tabBodies[tag]), get_get(self.tabBodies[tag]), 0, 2.5))
        # Change indicators
        self.selectedHead = tag
        self.selectedBody = self.tabBodies[tag]

