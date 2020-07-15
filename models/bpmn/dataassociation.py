import xml.etree.ElementTree as et

from models.bpmn.association import Association
from models.bpmn.enums.dataassocdirection import DataAssocDirection
from resources.namespaces import bpmn

class DataAssociation(Association):

    def __init__(self, **args):
        Association.__init__(self, **args)

        self.direction = self.expects(args, 'direction', DataAssocDirection.IN)

    def separate(self): pass

    def serialize(self):
        dataAssociationElement = et.Element(
            bpmn + 'data' + ('Input' if self.direction == DataAssocDirection.IN else 'Output') + 'Association')

        # target serialization
        targetElement = et.Element(bpmn + 'targetRef')
        targetElement.text = str (self.target.id)
        dataAssociationElement.append(targetElement)

        if self.direction == DataAssocDirection.IN:
            # source serialization
            if self.source != None:
                sourceElement = et.Element(bpmn + 'sourceRef')
                sourceElement.text = str (self.source.id)
                dataAssociationElement.append(sourceElement)

        return dataAssociationElement
