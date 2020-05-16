from models.bpmn.Linkable import Linkable
from models.bpmn.enums.GatewayType import GatewayType
from helpers.StringHelper import camelCase
import xml.etree.ElementTree as et


class Gateway(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.type: GatewayType = self.expects(
            args, 'type', GatewayType.Exclusive)

        self.ignore_attrs('type')

    def serialize(self):
        element = Linkable.serialize(self)
        element.tag = camelCase(self.type.name) + 'Gateway'
        return element