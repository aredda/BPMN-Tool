import xml.etree.ElementTree as et

from models.BPMNElement import BPMNElement


class Linkable(BPMNElement):

    IN = 1
    OUT = 2

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.incoming = []
        self.outgoing = []

    def add_link(self, linkable, direction=IN):
        if direction == Linkable.IN:
            self.incoming.append(linkable)
            linkable.outgoing.append(self)
        else:
            self.outgoing.append(linkable)
            linkable.incoming.append(self)

    def serialize(self):
        linkableElement = et.Element(self.__class__.__name__.lower())

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
