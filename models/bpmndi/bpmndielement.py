from models.xmlserializable import XMLSerializable
from xml.etree import ElementTree as et

class BPMNDIElement(XMLSerializable):

    def __init__(self, **args):

        self.id = args.get('id', None)
        self.element = args.get('element', None)

    def serialize(self):
        e = et.Element(self.__class__.__name__)

        if self.id != None: e.attrib['id'] = str (self.id)
        if self.element != None: e.attrib['bpmnElement'] = str (self.element.id)

        return e
