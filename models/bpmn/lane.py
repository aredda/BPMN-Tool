import xml.etree.ElementTree as et

from models.bpmn.container import Container
from resources.namespaces import bpmn

class Lane(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.process = self.expects(args, 'process', None)

        if self.process != None:
            self.process.add('lane', self)

    def serialize(self):
        laneElement = et.Element(bpmn + 'lane')

        for key in self.elements:
            for element in self.elements[key]:
                el = et.Element('flowNodeRef')
                el.text = element.id
                laneElement.append(el)

        return laneElement

    def add(self, name, item, addToProcess=True):
        Container.add(self, name, item)
        
        if addToProcess == True and self.process != None:
            self.process.add(name, item)
