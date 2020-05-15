import xml.etree.ElementTree as et
from models.BPMNElement import BPMNElement
from helpers.StringHelper import camelCase

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

    def serialize(self):
        element = et.Element (camelCase(self.__class__.__name__))
        # For each element in the dictionary of lists..
        for key in self.elements:
            if key != 'lane':
                for i in self.elements[key]:
                    element.append(i.serialize())

        return element