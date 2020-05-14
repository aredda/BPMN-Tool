from models.BPMNElement import BPMNElement

import xml.etree.ElementTree as et


class Flow(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.source = self.expects(args, "source")
        self.target = self.expects(args, "target")

    def serialize(self):
        def toLowerFirst(s): return s[:1].lower() + s[1:] if s else ''

        flowElement = et.Element(toLowerFirst(self.__class__.__name__))
        flowElement.attrib["sourceRef"] = self.source.id
        flowElement.attrib["targetRef"] = self.target.id

        return flowElement
