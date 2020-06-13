from models.bpmndi.bpmndielement import BPMNDIElement

class BPMNShape(BPMNDIElement):

    def __init__(self, **args):
        BPMNDIElement.__init__(self, **args)
        
        self.bounds = args.get('bounds', None)
        self.label = args.get('label', None)

    def serialize(self):
        e = BPMNDIElement.serialize(self)
        # bounds
        e.append(self.bounds.serialize())
        # label
        if self.label != None: e.append(self.label.serialize())
        # is horizontal
        if hasattr(self, 'isHorizontal') == True:
            e.attrib['isHorizontal'] = str(True)

        return e