import xml.etree.ElementTree as et

from resources.namespaces import *
from models.bpmn.container import Container

class Definitions(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.ignore_attrs('collaboration')

        self.elements['process'] = []
        self.elements['message'] = []

        self.collaboration = args.get('collaboration', None)

    def serialize(self):
        # register namespaces
        self.register_namespaces()

        # instantiate element
        element = Container.serialize(self)

        # Create a collaboration element
        collaboration = et.Element(bpmn + 'collaboration')
        collaboration.attrib['id'] = 'collaboration' if self.collaboration == None else self.collaboration

        # Append participants elements to collaboration element
        for process in self.elements['process']:
            participant = et.Element(bpmn + 'participant')

            participant.attrib['id'] = str (process.participant)
            participant.attrib['processRef'] = str (process.id)
            
            if process.name != None: 
                participant.attrib['name'] = str (process.name)

            collaboration.append(participant)

        # Append message flows to collaboration
        for message in self.elements['message']:
            collaboration.append(message.serialize())

        # Prepend collaboration
        element.insert(0, collaboration)

        return element

    # responsible for registring namespaces
    def register_namespaces(self):
        for prefix in namespaces.keys():
            et.register_namespace(prefix, namespaces[prefix])