import xml.etree.ElementTree as et

from models.Container import Container


class Lane(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.process = None

    def serialize(self):
        laneElement = et.Element("lane")
        laneElement.attrib["id"] = self.id

        return laneElement
