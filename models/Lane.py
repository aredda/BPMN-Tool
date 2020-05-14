import xml.etree.ElementTree as et

from models.Container import Container


class Lane(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.process = self.expects(args, 'process', None)

    def serialize(self):
        laneElement = et.Element("lane")

        for key in self.elements:
            for element in self.elements[key]:
                el = et.Element("flowNodeRef")
                el.text = element.id
                laneElement.append(el)

        return laneElement

    def add(self, name, item):
        Container.add(self, name, item)
        if self.process != None:
            self.process.add(name, item)
