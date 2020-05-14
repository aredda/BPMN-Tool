import xml.etree.ElementTree as et

from models.Flow import Flow
from models.enums.SequenceType import SequenceType


class SequenceFlow(Flow):

    def __init__(self, **args):
        Flow.__init__(self, **args)

        self.type = self.expects(args, "type")
