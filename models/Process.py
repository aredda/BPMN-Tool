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
                if "linkables" in lane.elements:
                    for element in lane.elements["linkables"]:
                        self.add("linkables", element)
                        el = et.Element("flowNodeRef")
                        el.text = element.id
                        laneElement.append(el)
                laneSetElement.append(laneElement)
            processElement.append(laneSetElement)

        self.serializeElements(processElement)
        return processElement

    def serializeElements(self, processElement):
        for element in self.elements["linkables"]:
            el = element.serialize()
            processElement.append(el)
