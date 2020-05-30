from models.bpmn.Event import Event
from models.bpmn.Task import Task
from models.bpmn.Process import Process
from models.bpmn.enums.EventType import EventType
from models.bpmn.enums.EventDefinition import EventDefinition
from helpers.stringhelper import to_pretty_xml
from models.bpmn.Lane import Lane
from models.bpmn.Gateway import Gateway

def run():
    
    p = Process(id='prc_main', name='Purchase Process')

    t1 = Task(id='tsk1', name='Requisition')
    t2 = Task(id='tsk2', name='Dispatch product')
    t3 = Task(id='tsk3', name='Buy Product')

    e1 = Event(id='evnt_start')
    e2 = Event(id='evnt_end', type=EventType.End)

    g1 = Gateway(id='gt1', name='Product is available?')
    g2 = Gateway(id='gt2')

    lane1 =  Lane(id='laneEmployee', name='Employee')
    lane2 =  Lane(id='laneWarehouse', name='Warehouse')
    lane3 =  Lane(id='lanePurchasing', name='Purchasing')

    p.add('lane', lane1, lane2, lane3)

    p.add('sequence', e1.add_link(t1, Task.OUT))
    p.add('sequence', t1.add_link(g1, Task.OUT))
    p.add('sequence', g1.add_link(g2, Task.OUT))
    p.add('sequence', g1.add_link(t3, Task.OUT))
    p.add('sequence', g2.add_link(t2, Task.OUT))
    p.add('sequence', t2.add_link(e2, Task.OUT))
    p.add('sequence', t3.add_link(g2, Task.OUT))

    lane1.add('event', e1)
    lane1.add('task', t1)
    lane2.add('gateway', g1)
    lane2.add('gateway', g2)
    lane2.add('event', e2)
    lane2.add('task', t2)
    lane3.add('task', t3)

    print (to_pretty_xml(p.serialize()))
