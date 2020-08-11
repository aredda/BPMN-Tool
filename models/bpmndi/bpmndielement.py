from xml.etree import ElementTree as et
from resources.namespaces import *
from helpers.stringhelper import generate_code
from models.xmlserializable import XMLSerializable

class BPMNDIElement(XMLSerializable):

    def __init__(self, **args):

        self.id = args.get('id', None)
        self.element = args.get('element', None)

    def serialize(self):
        e = et.Element(bpmndi + self.__class__.__name__)

        if self.element != None: 
            e.attrib['id'] = self.__class__.__name__ + '_' + generate_code() if not hasattr(self.element, 'id') else str (self.element.id) + '_di'

        if self.element != None: 
            e.attrib['bpmnElement'] = self.element if isinstance(self.element, str) else str (self.element.id)

        return e
