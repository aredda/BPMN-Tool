from models.bpmn.linkable import Linkable
from models.bpmn.enums.gatewaytype import GatewayType
from helpers.stringhelper import camel_case
from resources.namespaces import *

import xml.etree.ElementTree as et

class Gateway(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.type: GatewayType = self.expects(
            args, 'type', GatewayType.Exclusive)

        self.ignore_attrs('type')

    def serialize(self):
        element = Linkable.serialize(self)
        element.tag = bpmn + camel_case(self.type.name) + 'Gateway'
        return element
