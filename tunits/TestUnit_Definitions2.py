from helpers.StringHelper import toPrettyXml
from models.Event import Event
from models.Task import Task
from models.Process import Process
from models.Lane import Lane
from models.Gateway import Gateway
from models.SubProcess import SubProcess
from models.DataSotreReference import DataStoreReference
from models.Association import Association
from models.MessageFlow import MessageFlow
from models.Definitions import Definitions
from models.enums.EventType import EventType
from models.enums.EventDefinition import EventDefinition
from models.enums.DataAssocDirection import DataAssocDirection
from models.enums.TaskType import TaskType

def run():

    d = Definitions(author='Areda Ibrahim & Mohamed El Kalai')

    p1 = Process(id='prc_1', name='1st Approver', definitions=d)

    e1 = Event(id='evt_start_1', name='Approval Requested', definition=EventDefinition.Message)
    e2 = Event(id='evt_end_1', name='Task Completed', type=EventType.End)

    t1 = Task(id='tsk_1', name='evaluate request')
    t2 = Task(id='tsk_2', name='document and submit decision')

    p1.add ('task', t1, t2)
    p1.add ('event', e1, e2)

    print (toPrettyXml(d.serialize()))