import xml.etree.ElementTree as et

from models.Container import Container
from models.Lane import Lane


class Process(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

    def serialize(self):
        processElement = Container.serialize(self)

        if 'lane' in self.elements:
            laneSetElement = et.Element("laneSet")

            for lane in self.elements['lane']:
                laneElement = lane.serialize()
                laneSetElement.append(laneElement)

            processElement.append(laneSetElement)

        return processElement
