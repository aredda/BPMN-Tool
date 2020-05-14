import xml.etree.ElementTree as et

from models.Association import Association
from models.enums.DataAssocDirection import DataAssocDirection


class DataAssociation(Association):

    def __init__(self, **args):
        Association.__init__(self, **args)

        self.direction = self.expects(args, "direction")

    def serialize(self):
        dataAssociationElement = et.Element(
            'data' + ('Input' if self.direction == DataAssocDirection.IN else 'output') + 'Association')

        # if assoc is OUT => source = objectReference AND target = property
        # if assoc is IN => target = objectReference

        if self.direction == DataAssocDirection.IN:
            sourceElement = et.Element("sourceRef")
            sourceElement.text = self.source.id
            targetElement = et.Element('targetRef')
            targetElement.text = 'whatever'
            dataAssociationElement.append(sourceElement)
            dataAssociationElement.append(targetElement)

        targetElement = et.Element("targetRef")
        targetElement.text = self.target.id

        dataAssociationElement.append(targetElement)

        return dataAssociationElement
