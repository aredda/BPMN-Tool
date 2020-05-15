from models.XMLSerializable import XMLSerializable
from helpers.StringHelper import camelCase
import xml.etree.ElementTree as et


class BPMNElement(XMLSerializable):

    def __init__(self, **args):
        self.id = self.expects(args, 'id')
        self.name = self.expects(args, 'name')

    def expects(self, args, name, default=None):
        return default if name not in args else args[name]

    def configure(self, **args):
        """
        A setter for the element's attributes, and an alternative for the constructor
        """
        for key in args:
            if hasattr(self, key):
                setattr(self, args[key])

    # A default serialization
    def serialize(self):
        e = et.Element(camelCase(self.__class__.__name__))
        # Foreach property in class, add it as an attribute to the element
        for attr in vars(self):
            if getattr(self, attr) != None:
                e.attrib[attr] = str (getattr(self, attr))
        return e

    # toString
    def __str__(self):
        return str (self.id);