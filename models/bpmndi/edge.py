from models.bpmndi.bpmndielement import BPMNDIElement
from xml.etree import ElementTree as et

class BPMNEdge(BPMNDIElement):

    def __init__(self, **args):
        BPMNDIElement.__init__(self, **args)
        
        self.start = args['start']
        self.end = args['end']
        self.label = args.get('label', None)

    def serialize(self):
        e = BPMNDIElement.serialize(self)
        
        for point in [self.start, self.end]:
            ep = et.Element('waypoint')
            ep.attrib['x'] = str(point[0])
            ep.attrib['y'] = str(point[1])
            e.append(ep)

        if self.label != None: e.append(self.label.serialize())

        return e
            