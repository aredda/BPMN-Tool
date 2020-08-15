import xml.etree.ElementTree as et

from resources.namespaces import *
from helpers.stringhelper import generate_code
from models.bpmn.container import Container
from models.bpmn.lane import Lane

class Process(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.id = args.get('id', 'Process_' + generate_code())
        self.definitions = self.expects(args, 'definitions')
        self.participant = args.get('participant', 'Participant_' + generate_code())

        if self.definitions != None:
            self.definitions.add('process', self)

        self.ignore_attrs('definitions', 'participant')

    def serialize(self):
        processElement = Container.serialize(self)

        if 'lane' in self.elements:
            laneSetElement = et.Element(bpmn + "laneSet")

            for lane in self.elements['lane']:
                laneElement = lane.serialize()
                laneSetElement.append(laneElement)

            processElement.append(laneSetElement)

        return processElement

    def add(self, name, *items):
        super().add(name, *items)

        if name == 'lane':
            for lane in items:
                lane.process = self
