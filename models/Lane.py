import xml.etree.ElementTree as et

from models.Container import Container


class Lane(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.process = None

    def serialize(self):
        laneElement = et.Element("lane")

        if "linkables" in self.elements:
            for element in self.elements["linkables"]:
                el = et.Element("flowNodeRef")
                el.text = element.id
                laneElement.append(el)

        return laneElement
