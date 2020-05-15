from models.Linkable import Linkable
from models.enums.EventType import EventType
from models.enums.EventDefinition import EventDefinition
import xml.etree.ElementTree as et
from helpers.StringHelper import camelCase


class Event(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.type: EventType = self.expects(args, 'type', EventType.Start)
        self.definition = self.expects(
            args, 'definition', EventDefinition.Default)
        # true = interrupting; false = non-interrupting
        self.attachedTo = self.expects(args, 'attachedTo')
        self.cancelActivity = self.expects(args, 'cancelActivity', True)

        self.ignore_attrs('type', 'definition', 'attachedTo')

    def attach(self, activity):
        self.attachedTo = activity

    def __str__(self):
        return f'{self.type} - {self.definition}'

    def serialize(self):
        # Fix Tag Name
        eventElement = Linkable.serialize(self)
        eventElement.tag = ('boundary' if self.attachedTo !=
                            None else camelCase(self.type.name)) + 'Event'
        # Add Cancel Attribute
        if self.attachedTo != None:
            eventElement.attrib['cancelActivity'] = str(self.cancelActivity)
            eventElement.attrib['attachedToRef'] = str(self.attachedTo.id)
        # Add Definition Element
        if self.definition != EventDefinition.Default:
            eventDefElement = et.Element(camelCase(self.definition.name) + 'Definition')
            eventDefElement.attrib['id'] = f'{self.id}_{self.definition.name}Definition'
            eventElement.append(eventDefElement)

        return eventElement
