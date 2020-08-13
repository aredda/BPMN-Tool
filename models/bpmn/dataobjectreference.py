from models.bpmn.bpmnelement import BPMNElement
import xml.etree.ElementTree as et

class DataObjectReference(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.dataObject = self.expects(args, 'dataObject')

    def serialize(self):
        from resources.namespaces import bpmn
        element = BPMNElement.serialize(self)
        element.tag = bpmn + 'dataObjectReference'
        element.attrib.pop('dataObject')
        element.attrib['dataObjectRef'] = str(self.dataObject.id)
        return element

    def get_tag(self):
        return 'dataobjectreference'