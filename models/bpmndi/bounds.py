from models.xmlserializable import XMLSerializable
from xml.etree import ElementTree as et

class Bounds(XMLSerializable):
    
    # def __init__(self, coords: tuple, size: tuple):
    #     self.coords = coords
    #     self.size = size

    def __init__(self, **args):
        for key in args.keys():
            setattr(self, key, args[key])

    def serialize(self):
        e = et.Element('Bounds')

        e.attrib['x'] = str (self.x)
        e.attrib['y'] = str (self.y)
        e.attrib['width'] = str (self.width)
        e.attrib['height'] = str (self.height)

        return e