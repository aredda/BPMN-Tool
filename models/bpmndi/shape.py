from models.bpmndi.bpmndielement import BPMNDIElement

class BPMNShape(BPMNDIElement):

    def __init__(self, **args):
        BPMNDIElement.__init__(self, **args)
        
        self.bounds = args['bounds']
        self.label = args.get('label', None)

    def serialize(self):
        e = BPMNDIElement.serialize(self)
        e.append(self.bounds.serialize())
        if self.label != None: e.append(self.label.serialize())
        return e