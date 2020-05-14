from models.BPMNElement import BPMNElement
from helpers.StringHelper import camelCase

import xml.etree.ElementTree as et


class Flow(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.source = self.expects(args, "source")
        self.target = self.expects(args, "target")

    def serialize(self):
        flowElement = et.Element(camelCase(self.__class__.__name__))
        flowElement.attrib["sourceRef"] = self.source.id
        flowElement.attrib["targetRef"] = self.target.id

        return flowElement
