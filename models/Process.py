import xml.etree.ElementTree as et

from models.Container import Container
from models.Lane import Lane


class Process(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

    def add_lane(self, lane: Lane):
        self.add('lane', lane)
        lane.process = self

    def serialize(self):
        processElement = et.Element("process")

        for key in self.elements:
            if key == 'lane':
                laneSetElement = et.Element("laneSet")

                for lane in self.elements['lane']:
                    laneElement = lane.serialize()
                    laneSetElement.append(laneElement)

                processElement.append(laneSetElement)
            else:
                for i in self.elements[key]:
                    processElement.append(i.serialize())

        return processElement
