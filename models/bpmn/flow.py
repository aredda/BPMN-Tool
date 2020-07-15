from models.bpmn.bpmnelement import BPMNElement
from helpers.stringhelper import camel_case

import xml.etree.ElementTree as et

class Flow(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.source = self.expects(args, 'source')
        self.target = self.expects(args, 'target')

        self.ignore_attrs('source', 'target')

    def separate(self):
        self.source.remove_link(self)
        self.target.remove_link(self)

    def serialize(self):
        flowElement = BPMNElement.serialize(self)

        flowElement.attrib["sourceRef"] = self.source.id
        flowElement.attrib["targetRef"] = self.target.id

        return flowElement
