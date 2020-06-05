from models.bpmn.container import Container

class BPMNPlane(Container):
    
    def __init__(self, **args):
        Container.__init__(self, **args)
        self.ignore_attrs('element')
        self.element = args['element']

    def serialize(self):
        e = Container.serialize(self)
        e.tag = 'BPMNPlane'
        e.attrib['bpmnElement'] = str(self.element.id)

        return e


