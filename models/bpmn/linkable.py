import xml.etree.ElementTree as et

from models.bpmn.container import Container
from models.bpmn.dataobject import DataObject
from models.bpmn.datastorereference import DataStoreReference
from models.bpmn.enums.dataassocdirection import DataAssocDirection
from models.bpmn.property import Property
from models.bpmn.dataassociation import DataAssociation
from models.bpmn.sequenceflow import SequenceFlow


class Linkable(Container):

    IN = 1
    OUT = 2

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.incoming = []
        self.outgoing = []
        self.defaultFlow = self.expects(args, 'defaultFlow')

        self.ignore_attrs('incoming', 'outgoing', 'defaultFlow')

    # Responsible for linking two nodes/elements
    def add_link(self, linkable, direction=OUT):
        """
        Sets up a link with another linkable.
        Parameters:
            • linkable (Linkable): The linked object
            • direction (int): The direction of the link
        Returns:
            • SequenceFlow
        """
        # initialize an empty sequence
        seqFlow = SequenceFlow(
            id=f'seqFlow_{self.id}_{linkable.id}', source=linkable, target=self)
        # adjust link
        if direction == Linkable.IN:
            self.incoming.append(seqFlow)
            linkable.outgoing.append(seqFlow)
        else:
            # re-configure sequence flow
            seqFlow.configure(source=self, target=linkable)
            # finish configuration
            self.outgoing.append(seqFlow)
            linkable.incoming.append(seqFlow)
        # return the sequence of this link
        return seqFlow

    # Responsible for connecting a data entity to a linkable
    def link_data(self, data, direction):
        """
        Sets up a data association with a data object/data reference.
        Parameters:
            • data (DataObject | DataStoreReference): The linked data entity
            • direction (DataAssocDirection): The direction of the link
        """
        ref = data.reference if type(data) == data else data
        # an output assoc by default
        assoc = DataAssociation(target=ref, direction=direction)
        # If the direction is in then
        if direction == DataAssocDirection.IN:
            pty = Property()
            assoc = DataAssociation(
                id=f'dtAssoc_{self.id}_{data.id}', source=ref, target=pty, direction=direction)
            pty.id = 'pty_' + assoc.id
            self.add('property', pty)
        # add assoc to elements
        self.add('dataAssociation', assoc)

    # Overridding the functionality of serializing an element
    def serialize(self):
        linkableElement = Container.serialize(self)
        # If there is a default flow, then add it to the element as an attribute
        if self.defaultFlow != None:
            linkableElement.attrib['default'] = str(self.defaultFlow.id)

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
