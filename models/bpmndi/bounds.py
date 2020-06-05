from models.xmlserializable import XMLSerializable
from xml.etree import ElementTree as et

class Bounds(XMLSerializable):
    
    def __init__(self, coords: tuple, size: tuple):
        self.coords = coords
        self.size = size

    def serialize(self):
        e = et.Element('Bounds')

        e.attrib['x'] = str (self.coords[0])
        e.attrib['y'] = str (self.coords[1])
        e.attrib['width'] = str (self.size[0])
        e.attrib['height'] = str (self.size[1])

        return e