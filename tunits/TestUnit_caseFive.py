from helpers.StringHelper import toPrettyXml
from models.bpmn.Event import Event
from models.bpmn.Task import Task
from models.bpmn.Process import Process
from models.bpmn.Lane import Lane
from models.bpmn.Gateway import Gateway
from models.bpmn.SubProcess import SubProcess
from models.bpmn.DataSotreReference import DataStoreReference
from models.bpmn.Association import Association
from models.bpmn.enums.EventType import EventType
from models.bpmn.enums.EventDefinition import EventDefinition
from models.bpmn.enums.DataAssocDirection import DataAssocDirection

def run():

    p = Process(id='prc_1')
    sp1 = SubProcess(id='subprc_1', name='Perform Credit Check')

    e1 = Event(id='evt_start', name='Check Requested')
    e2 = Event(id='evt_check1', name='Credit Check Performed', type=EventType.IntermediateCatch, definition=EventDefinition.Signal)
    e3 = Event(id='evt_end', name='Credit Check Performed', type=EventType.End, definition=EventDefinition.Signal)

    t1 = Task(id='tsk1', name='Check for running instances')

    g = Gateway(id='gt1', name='Running instances of the same customer?')

    str1 = DataStoreReference(id='dtStr1')

    p.add('task', t1)
    p.add('event', e1, e2, e3)
    p.add('gateway', g)
    p.add('dataStore', str1)
    p.add('subProcess', sp1)

    e1.add_link(t1, Task.OUT)
    t1.add_link(g, Task.OUT)
    g.add_link(sp1, Task.OUT)
    g.add_link(e2, Task.OUT)
    e2.add_link(sp1, Task.OUT)
    sp1.add_link(e3, Task.OUT)

    t1.link_data(str1, DataAssocDirection.IN)

    print (toPrettyXml(p.serialize()))
    