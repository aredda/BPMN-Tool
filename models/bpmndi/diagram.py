from models.bpmn.container import Container

class BPMNDiagram(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

    def serialize(self):
        e = Container.serialize(self)
        e.tag = 'BPMNDiagram'

        return e