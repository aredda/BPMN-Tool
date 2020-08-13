import xml.etree.ElementTree as et

from resources.namespaces import *
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
from models.bpmn.messageflow import MessageFlow
from models.bpmn.datastorereference import DataStoreReference
from models.bpmn.dataobject import DataObject, DataObjectReference
from models.bpmn.association import Association
from models.bpmn.dataassociation import DataAssociation, DataAssocDirection
from models.bpmn.property import Property
from models.bpmn.lane import Lane
from models.bpmn.textannotation import TextAnnotation
from models.bpmndi.diagram import BPMNDiagram
from models.bpmndi.shape import BPMNShape
from models.bpmndi.edge import BPMNEdge
from models.bpmndi.bounds import Bounds
from models.bpmndi.label import BPMNLabel
from models.bpmndi.plane import BPMNPlane

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

    # bpmn_ns = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
    # bpmndi_ns = '{http://www.omg.org/spec/BPMN/20100524/DI}'
    # di_ns = '{http://www.omg.org/spec/DD/20100524/DI}'
    # dc_ns = '{http://www.omg.org/spec/DD/20100524/DC}'
    
    all_breeds = ['task', 'event', 'gateway', 'subprocess', 'flow', 'dataobject', 'dataobjectreference', 'datastorereference', 'textannotation', 'association']
    linkables = ['task', 'event', 'gateway', 'subprocess']

    di_breeds = ['BPMNEdge', 'BPMNShape']

    def __init__(self, root_element):
        # the root element which is actually a 'definitions' element
        self.root_element = root_element
        # a container of xml elements
        self.xelements = {}
        # a container of serialized elements
        self.selements = {}
        # a container of di elements
        self.delements = {}
        # a list container of all serialized elements
        self.all_elements = []
        # relation references
        self.relations = {}
        # an empty definitions object
        self.definitions = Definitions()
        # failed flow configurations
        self.failed_links = []
        # commencing deserialization operation
        self.prepare()
        self.instantiate()
        self.setup_collaboration()
        self.setup_message_flows()
        self.setup_lanes()
        self.setup_bpmndi()
        self.repair_failed()
        # self.clear_clutter()

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
        elif tag == 'textannotation': return TextAnnotation
        elif tag == 'BPMNShape': return BPMNShape
        elif tag == 'BPMNEdge': return BPMNEdge
        return None

    # find a serialized element by its id
    def find_element(self, id):
        for element in self.all_elements:
            if element.id == id:
                return element
            # process case
            if isinstance(element, Process):
                if element.participant == id:
                    return element
        return None

    def prepare(self):
        # a virtual process list
        processList = self.root_element.findall(bpmn + 'process')
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
                    tag = child.tag.split('}')[1].lower() if '}' in child.tag else child.tag.lower()
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
            if 'sub' in (process.tag.split('}')[1] if '}' in process.tag else process.tag).lower(): collection['isSubProcess'] = True
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
            # add it to the major list
            self.all_elements.append(process)
            # loop through children of process
            for breed in self.xelements['process'][p_id]['children'].keys():
                # for each element in this breed
                for e_id in self.xelements['process'][p_id]['children'][breed].keys():
                    # if there's no container for this breed add it
                    if breed not in children: children[breed] = {}
                    # retrieve xml element
                    xe = self.xelements['process'][p_id]['children'][breed][e_id]
                    xe_tag = xe.tag.split('}')[1].lower() if '}' in xe.tag else xe.tag.lower()
                    # instantiate an object
                    instance = (self.get_class(breed))(**xe.attrib)
                    # association settings
                    if breed == 'association':
                        instance.source = self.find_element(xe.attrib['sourceRef'])
                        instance.target = self.find_element(xe.attrib['targetRef'])
                    # type determinator for [Task - Event - Gateway]
                    def retrieve_type(breed, default):
                        # retrieve breed class
                        type_cls = EventType if breed == 'event' else (TaskType if breed == 'task' else GatewayType)
                        # retrieve type
                        instance_type = (xe.tag.split('}')[1] if '}' in xe.tag else xe.tag).lower().rstrip(breed)
                        # affect event
                        instance.type = get_enum(type_cls, instance_type if len(instance_type) > 0 else default)
                    # check if instance belongs to these breeds, then extract the type
                    defaults = {'task': 'default', 'event': 'start', 'gateway': 'exclusive'}
                    if breed in defaults.keys():
                        retrieve_type(breed, defaults[breed])
                    # activity flag settings
                    if breed in ['subprocess', 'task']:
                        self.setup_activity(xe, instance)
                    # event settings
                    if breed == 'event':
                        # definition extraction
                        event_definition = EventDefinition.Default
                        for child in xe: 
                            if 'definition' in child.tag.lower(): event_definition = get_enum(EventDefinition, (child.tag.split('}')[1] if '}' in child.tag else child.tag).lower().rstrip('eventdefinition'))
                        # setting up
                        instance.definition = event_definition
                    # flow settings
                    if breed == 'flow':
                        instance.source = self.find_element(xe.attrib['sourceRef'])
                        instance.target = self.find_element(xe.attrib['targetRef'])
                        # if linking is failed.. save it for later
                        if instance.source == None or instance.target == None:
                            # save the id of the targeted elements
                            instance.source, instance.target = xe.attrib['sourceRef'],xe.attrib['targetRef']
                            # mark as failed link/flow instance
                            self.failed_links.append(instance)
                        # check if it's a conditional flow
                        for child in xe:
                            if 'conditionExpression' in (child.tag.split('}')[1] if '}' in child.tag else child.tag).lower(): instance.type = SequenceType.CONDITIONAL  
                    # data object reference settings
                    if breed == 'dataobjectreference':
                        instance.dataObject = self.find_element(xe.attrib['dataObjectRef'])
                    # text annotation settings
                    if breed == 'textannotation':
                        instance.name = xe.find(bpmn + 'text').text
                    # add it to the children collection
                    children[breed][instance.id] = instance
                    # add it to the process container
                    process.add(breed, instance)
                    # add it to the major list
                    if breed == 'datastorereference':
                        print ('found a data store reference')
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
                        pure_tag = (child.tag.split('}')[1] if '}' in child.tag else child.tag).lower()
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
                                instance.target = self.find_element(child.find(bpmn + 'targetRef').text)
                            # check if this is a data input association
                            if pure_tag == 'datainputassociation':
                                # find property
                                xprop = xe.find(bpmn + 'property')
                                if self.find_element(xprop.attrib['id']) == None:
                                    # create a property
                                    prop = Property(**xprop.attrib)
                                    # add it to the linkable elements
                                    se.add('property', prop)
                                    # add it to the major list
                                    self.all_elements.append(prop)
                                # setting up the data assoc fields
                                instance.source = self.find_element(child.find(bpmn + 'sourceRef').text)
                                instance.target = self.find_element(xprop.attrib['id'])
                            # add element to the linkable's container
                            se.add('dataAssociation', instance)
                            # add element to the major list
                            self.all_elements.append(instance)
            # add it to the definition
            if isProcess == True: 
                self.definitions.add('process', process)
            else: 
                # configure subprocess before appending it
                self.setup_activity(xprocess, process)
                self.find_element(self.relations[process.id]).add('subprocess', process)
            # add it to the selements
            if 'process' not in self.selements: self.selements['process'] = {}
            # save it
            self.selements['process'][p_id] = {
                'instance': process,
                'children': children 
            }

    def setup_collaboration(self):
        # retrieve collaboration
        xcollaboration = self.root_element.find(bpmn + 'collaboration')
        # check if there's a collaboration object
        if xcollaboration == None: return
        # retrieve participants
        participants = {}
        for xchild in xcollaboration:
            if 'participant' in xchild.tag:
                # finish process's configuration
                self.find_element(xchild.attrib['processRef']).participant = xchild.attrib['id']
                # add to the tree
                participants[xchild.attrib['id']] = xchild
        # add collaboration to the tree
        self.xelements['collaboration'] = {
            'element': xcollaboration,
            'participants': participants
        }
        # adjust collaboration id
        self.definitions.collaboration = xcollaboration.attrib['id']

    def setup_lanes(self):
        # foreach process
        for p_id in self.xelements['process'].keys():
            # retrieve x element
            xprocess = self.xelements['process'][p_id]['element']
            # retrieve s element
            process = self.find_element(xprocess.attrib['id'])
            # retrieve lanes
            xLaneSet = xprocess.find(bpmn + 'laneSet')
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

    def setup_message_flows(self):
        # find collaboration element
        xcollaboration = self.root_element.find(bpmn + 'collaboration')
        # check if there's a collaboration
        if xcollaboration == None: return
        # find message flows
        for xflow in xcollaboration.findall(bpmn + 'messageflow'):
            # instantiate flow
            sflow = MessageFlow(**xflow.attrib)
            # configure flow
            sflow.source = self.find_element(xflow.attrib['sourceRef'])
            sflow.target = self.find_element(xflow.attrib['targetRef'])
            # add flow
            self.definitions.add('message', sflow)
            self.all_elements.append(sflow)

            print ('found a message flow: ' + sflow.id)

    def setup_bpmndi(self):
        # utilities
        def get_bounds(xelement):
            # retrieve x bounds element
            xbounds = xelement.find(dc + 'Bounds')
            # return bounds element
            return Bounds(**xbounds.attrib)
        # find the diagram xelement
        xdiagram = self.root_element.find(bpmndi + 'BPMNDiagram')
        # create a container for bpmndi elements
        diagram = BPMNDiagram(**xdiagram.attrib)
        # find plane
        xplane = xdiagram.find(bpmndi + 'BPMNPlane')
        # instantiate a plane object
        plane = BPMNPlane(**xplane.attrib)
        plane.element = self.find_element(xplane.attrib.get('bpmnElement', None))
        # save plane
        if plane.element == None:
            plane.element = str (xplane.attrib.get('bpmnElement', None))
        # fetch for di elements
        for breed in Deserializer.di_breeds:
            for xchild in xplane:
                if breed.lower() not in xchild.tag.lower():
                    continue
                # instantiate the object
                obj = (self.get_class(breed))(**xchild.attrib)
                # element reference
                obj.element = self.find_element(xchild.get('bpmnElement', None))
                # if object has a label
                xlabel = xchild.find(bpmndi + 'BPMNLabel')
                if xlabel != None: obj.label = BPMNLabel(bounds=get_bounds(xlabel))
                # shape settings
                if 'Shape' in xchild.tag:
                    # affect bounds
                    obj.bounds = get_bounds(xchild)
                    # adjusting reference for process
                    if obj.element == None:
                        obj.element = xchild.attrib['bpmnElement']
                        obj.isHorizontal = True
                # edge settings
                if 'Edge' in xchild.tag:
                    print ('setting up an edge')
                    # retrieve waypoints
                    xpoints = xchild.findall(di + 'waypoint')
                    # affecting points
                    obj.start = (xpoints[0].attrib['x'], xpoints[0].attrib['y'])
                    obj.end = (xpoints[-1].attrib['x'], xpoints[-1].attrib['y'])
                # add it to the plane container
                plane.add((xchild.tag.split('}')[1] if '}' in xchild.tag else xchild.tag).lower() , obj)
                # save this di element by its element's id to facilitate retrieval later
                self.delements[xchild.attrib['bpmnElement']] = obj
        # add the plane to diagram
        diagram.add('plane', plane)
        # add the di diagram to the definitions
        self.definitions.add('di', diagram)

    def setup_activity(self, xelement, instance):
        # get tag
        xe_tag = (xelement.tag.split('}')[1] if '}' in xelement.tag else xelement.tag).lower()
        # default activity flag
        activity_flag = ActivityFlag.Default
        # check if this activity is flagged as adhoc
        if 'adhoc' in xe_tag:
            activity_flag = ActivityFlag.AdHoc
        # check if this activity is flaffed as a looped one
        for child in xelement:
            # retrieve purified tag
            child_tag = (child.tag.split('}')[1] if '}' in child.tag else child.tag).lower()
            # check if this is a loop flag
            if 'loopcharacteristics' in child_tag:
                if 'standard' in child_tag: 
                    activity_flag = ActivityFlag.Loop
                if 'multiinstance' in child_tag: 
                    activity_flag = ActivityFlag.ParallelMultiple
                    if 'isSequential' in child.attrib:
                        activity_flag = ActivityFlag.SequentialMultiple
        # affecting flag
        instance.flag = activity_flag

    def clear_clutter(self):
        to_delete = []
        # search for extra needless data objects
        for e in self.all_elements:
            if type(e) == DataObject:
                found = False
                for f in self.all_elements:
                    if type(f) == DataObjectReference:
                        if f.dataObject == e: found = True
                if found == False:
                    to_delete.append (e)
        # clear found elements
        for e in to_delete:
            # clear it from the major list
            self.all_elements.remove(e)
            # clear it from processes
            for process in self.selements['process'].keys():
                self.selements['process'][process]['instance'].remove('dataobject', e)
    
    def repair_failed(self):
        for instance in self.failed_links:
            # retrieve references
            sourceRef, targetRef = instance.source, instance.target
            # find references
            instance.source, instance.target = self.find_element(sourceRef), self.find_element(targetRef)