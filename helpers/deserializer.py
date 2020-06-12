import xml.etree.ElementTree as et

from helpers.stringhelper import to_pretty_xml
from models.bpmn.definitions import Definitions
from models.bpmn.process import Process
from models.bpmn.task import Task, TaskType
from models.bpmn.event import Event, EventDefinition, EventType
from models.bpmn.gateway import Gateway, GatewayType
from models.bpmn.sequenceflow import SequenceFlow, SequenceType

# xelements: data schema
# {
#     'id': {
#         'element': ...,
#         'children': {
#             'breed1': {
#                   'id': ...
#              }
#         }
#     }
# }

# selements: data schema
# [
#     'id' {
#         'instance': ...,

#     }
# ]

class Deserializer:

    bpmn_ns = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
    
    all_breeds = ['task', 'event', 'gateway', 'subprocess', 'flow', 'data', 'association']
    linkables = ['task', 'event', 'gateway', 'subprocess']
    flows = ['flow', 'association']

    def __init__(self, root_tree):
        # the root element which is actually a 'definitions' element
        self.root_element = root_tree.getroot()
        # a container of xml elements
        self.xelements = {}
        # a container of serialized elements
        self.selements = {}
        self.all_elements = []
        # an empty definitions object
        self.definitions = Definitions()

    def get_class(self, tag):
        if tag == 'task': return Task
        elif tag == 'event': return Event
        elif tag == 'gateway': return Gateway
        elif tag == 'flow': return SequenceFlow

        return None

    def find_element(self, id):
        for element in self.all_elements:
            if element.id == id:
                return element
        return None

    def prepare(self):
        # retrieve process elements
        for process in self.root_element.findall(Deserializer.bpmn_ns + 'process'):
            # if there's no process collection
            if 'process' not in self.xelements:
                self.xelements['process'] = {}
            # initialize a collection
            collection = {
                'element': process,
                'children': {}
            }
            children = {}
            # search for breeds
            for breed in Deserializer.all_breeds:
                for child in process:
                    # purify tag 
                    tag = child.tag.split('}')[1].lower()
                    # if this element belongs to this breed we're looking for
                    if breed in tag:
                        # add this element to the breed's collection
                        if breed not in children:
                            children[breed] = {}
                        children[breed][child.attrib['id']] = child
            # attach children to collection
            collection['children'] = children
            # add process element to the list of elements
            self.xelements['process'][process.attrib['id']] = collection

    def instantiate(self):
        # foreach process in xelements
        for p_id in self.xelements['process'].keys():
            # extract the xml element
            xprocess = self.xelements['process'][p_id]['element']
            # selements children
            children = {}
            # instantiate a process element
            process = Process(**xprocess.attrib)
            # loop through children of process
            for breed in self.xelements['process'][p_id]['children'].keys():
                if breed in ['data', 'association']: continue
                for e_id in self.xelements['process'][p_id]['children'][breed].keys():
                    # if there's no container for this breed add it
                    if breed not in children: children[breed] = {}
                    # retrieve xml element
                    xe = self.xelements['process'][p_id]['children'][breed][e_id]
                    # instantiate an object
                    instance = (self.get_class(breed))(**xe.attrib)
                    # flow settings
                    if breed == 'flow':
                        instance.source = self.find_element(xe.attrib['sourceRef'])
                        instance.target = self.find_element(xe.attrib['targetRef'])
                    # add it to the children collection
                    children[breed][instance.id] = instance
                    # add it to the process container
                    process.add(breed, instance)
                    # add it to the major list
                    self.all_elements.append(instance)
            # set up flows
            for breed in Deserializer.linkables:
                if breed not in children: continue
                for e_id in children[breed].keys():
                    # retrieve xml element
                    xe = self.xelements['process'][p_id]['children'][breed][e_id]
                    # retrieve instance
                    se = children[breed][e_id]
                    # loop through its elements
                    for child in xe:
                        # purify tag name
                        pure_tag = child.tag.split('}')[1].lower()
                        # append the sequence flow to the incoming or ougoing list
                        if hasattr(se, pure_tag):
                            getattr(se, pure_tag).append(self.find_element(child.text))
            # add it to the definition
            self.definitions.add('process', process)
            # add it to the major list
            self.all_elements.append(process)
            # add it to the selements
            if 'process' not in self.selements: 
                self.selements['process'] = {}
            # save it
            self.selements['process'][p_id] = {
                'instance': process,
                'children': children 
            }
