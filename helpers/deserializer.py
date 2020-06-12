import xml.etree.ElementTree as et

from helpers.reflector import get_enum
from helpers.stringhelper import to_pretty_xml
from models.bpmn.definitions import Definitions
from models.bpmn.process import Process
from models.bpmn.subprocess import SubProcess
from models.bpmn.enums.activityflag import ActivityFlag
from models.bpmn.task import Task, TaskType
from models.bpmn.event import Event, EventDefinition, EventType
from models.bpmn.gateway import Gateway, GatewayType
from models.bpmn.sequenceflow import SequenceFlow, SequenceType
from models.bpmn.datastorereference import DataStoreReference
from models.bpmn.dataobject import DataObject, DataObjectReference
from models.bpmn.association import Association
from models.bpmn.dataassociation import DataAssociation, DataAssocDirection
from models.bpmn.property import Property
from models.bpmn.lane import Lane

# data schema
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

class Deserializer:

    bpmn_ns = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
    
    all_breeds = ['task', 'event', 'gateway', 'subprocess', 'flow', 'dataobject', 'dataobjectreference', 'datastorereference', 'association']
    linkables = ['task', 'event', 'gateway', 'subprocess']

    def __init__(self, root_tree):
        # the root element which is actually a 'definitions' element
        self.root_element = root_tree.getroot()
        # a container of xml elements
        self.xelements = {}
        # a container of serialized elements
        self.selements = {}
        # a list container of all serialized elements
        self.all_elements = []
        # relation references
        self.relations = {}
        # an empty definitions object
        self.definitions = Definitions()
        # commencing deserialization operation
        self.prepare()
        self.instantiate()
        self.setup_lanes()

    # type router
    def get_class(self, tag):
        if tag == 'task': return Task
        elif tag == 'event': return Event
        elif tag == 'gateway': return Gateway
        elif tag == 'flow': return SequenceFlow
        elif tag == 'subprocess': return SubProcess
        elif tag == 'datastorereference': return DataStoreReference
        elif tag == 'dataobjectreference': return DataObjectReference
        elif tag == 'dataobject': return DataObject
        elif tag == 'association': return Association
        elif tag == 'dataoutputassociation' or tag == 'datainputassociation': return DataAssociation
        return None

    # find a serialized element by its id
    def find_element(self, id):
        for element in self.all_elements:
            if element.id == id:
                return element
        return None

    def prepare(self):
        # a virtual process list
        processList = self.root_element.findall(Deserializer.bpmn_ns + 'process')
        # retrieve process elements
        for process in processList:
            # store id
            processRef = process.attrib['id']
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
                    # if this child is subprocess
                    if 'sub' in tag:
                        if child not in processList:
                            processList.append(child) 
                            self.relations[child.attrib['id']] = processRef
                    # if this element belongs to this breed we're looking for
                    elif breed in tag:
                        # add this element to the breed's collection
                        if breed not in children:
                            children[breed] = {}
                        children[breed][child.attrib['id']] = child
            # attach children to collection
            collection['children'] = children
            # if this element is a subprocess then mark it
            if 'sub' in process.tag.split('}')[1].lower(): collection['isSubProcess'] = True
            # add process element to the list of elements
            self.xelements['process'][processRef] = collection

    def instantiate(self):
        # foreach process in xelements
        for p_id in self.xelements['process'].keys():
            # extract the xml element
            xprocess = self.xelements['process'][p_id]['element']
            # indicating if this element is a process
            isProcess = not self.xelements['process'][p_id].get('isSubProcess', False)
            # retrieve the appropriate class
            process_class = SubProcess if isProcess == False else Process
            # selements children
            children = {}
            # instantiate a process element
            process = process_class(**xprocess.attrib)
            # loop through children of process
            for breed in self.xelements['process'][p_id]['children'].keys():
                # for each element in this breed
                for e_id in self.xelements['process'][p_id]['children'][breed].keys():
                    # if there's no container for this breed add it
                    if breed not in children: children[breed] = {}
                    # retrieve xml element
                    xe = self.xelements['process'][p_id]['children'][breed][e_id]
                    xe_tag = xe.tag.split('}')[1].lower()
                    # instantiate an object
                    instance = (self.get_class(breed))(**xe.attrib)
                    # subprocess settings
                    if breed == 'subprocess':
                        pass
                    # type determinator for [Task - Event - Gateway]
                    def retrieve_type(breed, default):
                        # retrieve breed class
                        type_cls = EventType if breed == 'event' else (TaskType if breed == 'task' else GatewayType)
                        # retrieve type
                        instance_type = xe.tag.split('}')[1].lower().rstrip(breed)
                        # affect event
                        instance.type = get_enum(type_cls, instance_type if len(instance_type) > 0 else default)
                    # check if instance belongs to these breeds, then extract the type
                    defaults = {'task': 'default', 'event': 'start', 'gateway': 'exclusive'}
                    if breed in defaults.keys():
                        retrieve_type(breed, defaults[breed])
                    # activity flag settings
                    if breed in ['subprocess', 'task']:
                        # default activity flag
                        activity_flag = ActivityFlag.Default
                        # check if this activity is flagged as adhoc
                        if 'adhoc' in xe_tag: activity_flag = ActivityFlag.AdHoc
                        # check if this activity is flaffed as a looped one
                        for child in xe:
                            # retrieve purified tag
                            child_tag = child.tag.split('}')[1].lower()
                            # check if this is a loop flag
                            if 'loopcharacteristics' in child_tag:
                                if 'standard' in child_tag: activity_flag = ActivityFlag.Loop
                                if 'multiinstance' in child_tag: 
                                    activity_flag = ActivityFlag.ParallelMultiple
                                    if 'isSequential' in child.attrib:
                                        activity_flag = ActivityFlag.SequentialMultiple
                        # affecting flag
                        instance.flag = activity_flag
                    # event settings
                    if breed == 'event':
                        # definition extraction
                        event_definition = EventDefinition.Default
                        for child in xe: 
                            if 'definition' in child.tag.lower(): event_definition = get_enum(EventDefinition, child.tag.split('}')[1].lower().rstrip('eventdefinition'))
                        # setting up
                        instance.definition = event_definition
                    # flow settings
                    if breed == 'flow':
                        instance.source = self.find_element(xe.attrib['sourceRef'])
                        instance.target = self.find_element(xe.attrib['targetRef'])
                        # check if it's a conditional flow
                        for child in xe:
                            if 'conditionExpression' in child.tag.split('}')[1].lower(): instance.type = SequenceType.CONDITIONAL  
                    # data object reference settings
                    if breed == 'dataobjectreference':
                        instance.dataObject = self.find_element(xe.attrib['dataObjectRef'])
                    # add it to the children collection
                    children[breed][instance.id] = instance
                    # add it to the process container
                    process.add(breed, instance)
                    # add it to the major list
                    self.all_elements.append(instance)
            # set up flows & associations
            for breed in Deserializer.linkables:
                if breed not in children: continue
                # foreach element in this linkable breed
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
                        # if this child is an association
                        if 'association' in pure_tag:
                            # create an association instance
                            instance = self.get_class(pure_tag)(**child.attrib)
                            instance.direction = DataAssocDirection.IN if pure_tag == 'datainputassociation' else DataAssocDirection.OUT
                            # check if this is a data output association
                            if pure_tag == 'dataoutputassociation':
                                instance.target = self.find_element(child.find(Deserializer.bpmn_ns + 'targetRef').text)
                            # check if this is a data input association
                            if pure_tag == 'datainputassociation':
                                # find property
                                xprop = xe.find(Deserializer.bpmn_ns + 'property')
                                if self.find_element(xprop.attrib['id']) == None:
                                    # create a property
                                    prop = Property(**xprop.attrib)
                                    # add it to the linkable elements
                                    se.add('property', prop)
                                    # add it to the major list
                                    self.all_elements.append(prop)
                                # setting up the data assoc fields
                                instance.source = self.find_element(child.find(Deserializer.bpmn_ns + 'sourceRef').text)
                                instance.target = self.find_element(xprop.attrib['id'])
                            # add element to the linkable's container
                            se.add('dataAssociation', instance)
            # add it to the definition
            if isProcess == True: self.definitions.add('process', process)
            else: self.find_element(self.relations[process.id]).add('subprocess', process)
            # add it to the major list
            self.all_elements.append(process)
            # add it to the selements
            if 'process' not in self.selements: self.selements['process'] = {}
            # save it
            self.selements['process'][p_id] = {
                'instance': process,
                'children': children 
            }

    def setup_lanes(self):
        # foreach process
        for p_id in self.xelements['process'].keys():
            # retrieve x element
            xprocess = self.xelements['process'][p_id]['element']
            # retrieve s element
            process = self.find_element(xprocess.attrib['id'])
            # retrieve lanes
            xLaneSet = xprocess.find(Deserializer.bpmn_ns + 'laneSet')
            # check if there's a laneset
            if xLaneSet != None:
                # loop through lanes
                for xlane in xLaneSet:
                    # a lane instance
                    slane = Lane(**xlane.attrib)
                    slane.process = process
                    # retrieve all lane elements
                    for xNodeRef in xlane:
                        slane.add('node', self.find_element(xNodeRef.text), False)
                    # add the lane to process
                    process.add('lane', slane)