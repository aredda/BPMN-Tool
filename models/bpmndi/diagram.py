from models.bpmn.container import Container
from resources.namespaces import *

class BPMNDiagram(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

    def serialize(self):
        e = Container.serialize(self)
        e.tag = bpmndi + 'BPMNDiagram'

        return e