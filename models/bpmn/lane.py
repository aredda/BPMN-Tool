import xml.etree.ElementTree as et

from helpers.stringhelper import generate_code
from models.bpmn.container import Container
from resources.namespaces import bpmn

class Lane(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.id = args.get('id', 'lane_' + generate_code())
        self.process = self.expects(args, 'process', None)

        if self.process != None:
            self.process.add('lane', self)

    def serialize(self):
        laneElement = et.Element(bpmn + 'lane')
        laneElement.attrib['id'] = self.id

        for key in self.elements:
            for element in self.elements[key]:
                el = et.Element('flowNodeRef')
                el.text = element.id
                laneElement.append(el)

        return laneElement

    def add(self, name, item, addToProcess=True):
        if item.get_tag() not in ['sequenceflow']:
            Container.add(self, name, item)
        
        if addToProcess == True and self.process != None:
            self.process.add(name, item)

    def remove(self, tag, child):
        super().remove(tag, child)
        # remove from the process as well
        self.process.remove(tag, child)

    def get_tag(self): return 'lane'