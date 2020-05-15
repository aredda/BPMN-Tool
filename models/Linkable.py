import xml.etree.ElementTree as et

from models.Container import Container
from models.DataObject import DataObject
from models.DataSotreReference import DataStoreReference
from models.enums.DataAssocDirection import DataAssocDirection
from models.Property import Property
from models.DataAssociation import DataAssociation

class Linkable(Container):

    IN = 1
    OUT = 2

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.incoming = []
        self.outgoing = []
        self.defaultFlow = self.expects(args, 'defaultFlow')

    def add_link(self, linkable, direction=IN):
        if direction == Linkable.IN:
            self.incoming.append(linkable)
            linkable.outgoing.append(self)
        else:
            self.outgoing.append(linkable)
            linkable.incoming.append(self)

    def link_data(self, dataObject, direction):
        ref = dataObject.reference if type(dataObject) == DataObject else dataObject
        # an output assoc by default
        assoc = DataAssociation(target=ref, direction=direction)
        # If the direction is in then
        if direction == DataAssocDirection.IN:
            pty = Property()
            assoc = DataAssociation(id=f'dtAssoc_{self.id}_{dataObject.id}', source=ref, target=pty, direction=direction)
            pty.id = 'pty_' + assoc.id
            self.add('property', pty)
        # add assoc to elements
        self.add('dataAssociation', assoc)

    def serialize(self):
        linkableElement = Container.serialize(self)
        # If there is a default flow, then add it to the element as an attribute
        if self.defaultFlow != None:
            linkableElement.attrib['default'] = str (self.defaultFlow.id)

        lists = [
            {'name': 'incoming', 'list': self.incoming},
            {'name': 'outgoing', 'list': self.outgoing}
        ]

        for setting in lists:
            for item in setting['list']:
                inElement = et.Element(setting['name'])
                inElement.text = str(item.id)
                linkableElement.append(inElement)

        return linkableElement
