import xml.etree.ElementTree as et

from models.Container import Container
from models.Lane import Lane


class Process(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.lanes = []

    def add_lane(self, lane: Lane):
        self.lanes.append(lane)
        lane.process = self

    def serialize(self):
        processElement = et.Element("process")

        if len(self.lanes) != 0:
            laneSetElement = et.Element("laneSet")

            for lane in self.lanes:
                laneElement = lane.serialize()
                self.serializeElements(lane.elements, processElement)
                laneSetElement.append(laneElement)

            processElement.append(laneSetElement)

        else:
            self.serializeElements(self.elements, processElement)

        return processElement

    def serializeElements(self, elements, processElement):
        if "linkables" in elements:
            for element in elements["linkables"]:
                el = element.serialize()
                processElement.append(el)
