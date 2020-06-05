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

    e1 = Event(id='evt_start_1', name='Approval Requested', definition=EventDefinition.Message)
    e2 = Event(id='evt_end_1', name='Task Completed', type=EventType.End)

    t1 = Task(id='tsk_1', name='evaluate request')
    t2 = Task(id='tsk_2', name='document and submit decision')

    p1.add ('task', t1, t2)
    p1.add ('event', e1, e2)

    print (to_pretty_xml(d.serialize()))