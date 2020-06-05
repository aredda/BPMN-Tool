from models.bpmndi.bpmndielement import BPMNDIElement
from xml.etree import ElementTree as et

class BPMNLabel(BPMNDIElement):

    def __init__(self, **args):
        BPMNDIElement.__init__(self, **args)

        self.bounds = args.get('bounds', None)

    def serialize(self):
        e = BPMNDIElement.serialize(self)
        e.append(self.bounds.serialize())
        return e