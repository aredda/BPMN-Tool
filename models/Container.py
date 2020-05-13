from models.BPMNElement import BPMNElement

class Container(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.elements = {}

    def add(self, name, item):
        # Initialize an empty list
        if name not in self.elements:
            self.elements[name] = []
        # Add element
        self.elements[name].append(item)