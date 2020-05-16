import xml.etree.ElementTree as et
from models.Container import Container

class Definitions(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.elements['process'] = []
        self.elements['message'] = []

    def serialize(self):
        element = Container.serialize(self)

        # Create a collaboration element
        collaboration = et.Element('collaboration')
        collaboration.attrib['id'] = 'collaboration'

        # Append participants elements to collaboration element
        for process in self.elements['process']:
            participant = et.Element('participant')

            participant.attrib['id'] = 'participant_' + str (self.elements['process'].index (process))
            participant.attrib['name'] = str (process.name)
            participant.attrib['processRef'] = str (process.id)

            collaboration.append(participant)

        # Append message flows to collaboration
        for message in self.elements['message']:
            collaboration.append(message.serialize())

        # Prepend collaboration
        element.insert(0, collaboration)

        return element