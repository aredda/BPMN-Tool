import xml.etree.ElementTree as et

from models.bpmn.association import Association
from models.bpmn.enums.dataassocdirection import DataAssocDirection


class DataAssociation(Association):

    def __init__(self, **args):
        Association.__init__(self, **args)

        self.direction = self.expects(args, "direction", DataAssocDirection.IN)

    def serialize(self):
        dataAssociationElement = et.Element(
            'data' + ('Input' if self.direction == DataAssocDirection.IN else 'Output') + 'Association')

        # target serialization
        targetElement = et.Element('targetRef')
        targetElement.text = str (self.target.id)
        dataAssociationElement.append(targetElement)

        if self.direction == DataAssocDirection.IN:
            # source serialization
            if self.source != None:
                sourceElement = et.Element("sourceRef")
                sourceElement.text = str (self.source.id)
                dataAssociationElement.append(sourceElement)

        return dataAssociationElement
