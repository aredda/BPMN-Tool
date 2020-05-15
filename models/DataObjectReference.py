from models.BPMNElement import BPMNElement
import xml.etree.ElementTree as et

class DataObjectReference(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.dataObject = self.expects(args, 'dataObject')

    def serialize(self):
        element = BPMNElement.serialize(self)
        element.attrib.pop('dataObject')
        element.attrib['dataObjectRef'] = str(self.dataObject.id)
        return element