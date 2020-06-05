from helpers.stringhelper import to_pretty_xml
from models.bpmn.event import Event
from models.bpmn.task import Task
from models.bpmn.process import Process
from models.bpmn.lane import Lane
from models.bpmn.gateway import Gateway
from models.bpmn.subprocess import SubProcess
from models.bpmn.DataSotreReference import DataStoreReference
from models.bpmn.association import Association
from models.bpmn.messageflow import MessageFlow
from models.bpmn.definitions import Definitions
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition
from models.bpmn.enums.dataassocdirection import DataAssocDirection
from models.bpmn.enums.tasktype import TaskType

def run():

    d = Definitions(author='Areda Ibrahim & Mohamed El Kalai')

    p1 = Process(id='prc_1', name='1st Approver', definitions=d)
    p2 = Process(id='prc_2', name='Process Engine', definitions=d)
    p3 = Process(id='prc_3', name='2nd Approver', definitions=d)

    e1 = Event(id='evt_start_1', name='Approval Requested', definition=EventDefinition.Message)
    e2 = Event(id='evt_end_1', name='Task Completed', type=EventType.End)

    t1 = Task(id='tsk_1', name='evaluate request')
    t2 = Task(id='tsk_2', name='document and submit decision')

    e4 = Event(id='evt_start_2', name='Approval Requested')
    e5 = Event(id='evt_end_2', name='Request Rejected <First Stage>', type=EventType.End)
    e6 = Event(id='evt_end_3', name='Request Rejected <Second Stage>', type=EventType.End)
    e7 = Event(id='evt_end_4', name='Request Approved', type=EventType.End)

    g1 = Gateway(id='gt_1', name='approved')
    g2 = Gateway(id='gt_2', name='approved')

    t3 = Task(id='tsk_3', type=TaskType.User, name='Decide on approval <1st stage>')    
    t4 = Task(id='tsk_4', type=TaskType.User, name='Decide on approval <2nd stage>')    

    e8 = Event(id='evt_start_3', name='Approval requested', definition=EventDefinition.Message)
    e9 = Event(id='evt_end_5', type=EventType.End, name='Task completed')

    t5 = Task(id='tsk_5', name='evaluate request') 
    t6 = Task(id='tsk_5', name='document and submit decision') 

    # Appending
    p1.add ('task', t1, t2)
    p1.add ('event', e1, e2)

    p2.add ('task', t3, t4)
    p2.add ('event', e4, e5, e6, e7)
    p2.add ('gateway', g1, g2)

    p3.add ('task', t5, t6)
    p3.add ('event', e8, e9)

    # Linking
    p1.add ('sequence', e1.add_link(t1))
    p1.add ('sequence', t1.add_link(t2))
    p1.add ('sequence', t2.add_link(e2))

    p2.add ('sequence', e4.add_link(t3))
    p2.add ('sequence', t3.add_link(g1))
    p2.add ('sequence', g1.add_link(t4))
    p2.add ('sequence', g1.add_link(e5))
    p2.add ('sequence', t4.add_link(g2))
    p2.add ('sequence', g2.add_link(e6))
    p2.add ('sequence', g2.add_link(e7))

    p3.add ('sequence', e8.add_link(t5))
    p3.add ('sequence', t5.add_link(t6))
    p3.add ('sequence', t6.add_link(e9))

    d.add('message', MessageFlow(source=t3, target=e1))
    d.add('message', MessageFlow(source=t2, target=t3))
    d.add('message', MessageFlow(source=t4, target=e8))
    d.add('message', MessageFlow(source=t6, target=t4))

    print (to_pretty_xml(d.serialize()))