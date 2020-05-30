from helpers.stringhelper import to_pretty_xml
from models.bpmn.Event import Event
from models.bpmn.Task import Task
from models.bpmn.Process import Process
from models.bpmn.Lane import Lane
from models.bpmn.Gateway import Gateway
from models.bpmn.SubProcess import SubProcess
from models.bpmn.DataSotreReference import DataStoreReference
from models.bpmn.Association import Association
from models.bpmn.MessageFlow import MessageFlow
from models.bpmn.Definitions import Definitions
from models.bpmn.enums.EventType import EventType
from models.bpmn.enums.EventDefinition import EventDefinition
from models.bpmn.enums.DataAssocDirection import DataAssocDirection
from models.bpmn.enums.TaskType import TaskType

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