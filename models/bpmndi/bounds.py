from xml.etree import ElementTree as et
from models.xmlserializable import XMLSerializable
from resources.namespaces import *

class Bounds(XMLSerializable):

    def __init__(self, **args):
        for key in args.keys():
            setattr(self, key, args[key])

    def serialize(self):
        e = et.Element(dc + 'Bounds')

        e.attrib['x'] = str (self.x)
        e.attrib['y'] = str (self.y)
        e.attrib['width'] = str (self.width)
        e.attrib['height'] = str (self.height)

        return e