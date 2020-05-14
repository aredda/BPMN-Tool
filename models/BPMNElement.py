from models.XMLSerializable import XMLSerializable
from helpers.StringHelper import camelCase
import xml.etree.ElementTree as et

class BPMNElement(XMLSerializable):

    def __init__(self, **args):
        self.id = self.expects(args, 'id')      
        self.name = self.expects(args, 'name')

    def expects(self, args, name, default = None):
        return default if name not in args else args[name]

    def __str__(self):
        return str (self.id);

    def serialize(self):
        e = et.Element(camelCase(self.__class__.__name__))
        # Foreach property in class, add it as an attribute to the element
        for attr in vars(self):
            if getattr(self, attr) != None:
                e.attrib[attr] = str (getattr(self, attr))
        return e