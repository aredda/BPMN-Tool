from models.bpmn.container import Container

class BPMNPlane(Container):
    
    def __init__(self, **args):
        Container.__init__(self, **args)
        
        self.ignore_attrs('element')
        self.element = args.get('element', None)

    def serialize(self):
        e = Container.serialize(self)
        e.tag = 'BPMNPlane'
        if self.element != None: 
            e.attrib['bpmnElement'] = self.element if isinstance(self.element, str) else str(self.element.id)

        return e


