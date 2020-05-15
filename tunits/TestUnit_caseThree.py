from models.Event import Event
from models.Task import Task
from models.SubProcess import SubProcess
from models.Process import Process
from models.enums.EventType import EventType
from models.enums.EventDefinition import EventDefinition
from helpers.StringHelper import toPrettyXml


def run():

    # Instanciation section

    p = Process(id='prc', name='participant1')
    sp = SubProcess(name='Evaluate Grans')

    e1 = Event(id='event_start', type=EventType.Start,
               definition=EventDefinition.Conditional)
    e2 = Event(id='event_compensation', type=EventType.IntermediateCatch,
               definition=EventDefinition.Compensation)
    e3 = Event(id='event_timer', type=EventType.IntermediateCatch,
               definition=EventDefinition.Timer)
    e4 = Event(id='event_error', type=EventType.IntermediateCatch,
               definition=EventDefinition.Error)
    e5 = Event(id='event_end', type=EventType.End,
               definition=EventDefinition.Message)

    t1 = Task(id='task_develop', name='Develop Criteria')
    t2 = Task(id='task_record', name='Record')
    t3 = Task(id='task_roll', name='Roll out Record')
    t4 = Task(id='task_timeout', name='Timeout Error')
    t5 = Task(id='task_any', name='Any Exception')

    # Links section

    p.add('subprocess', sp)
    p.add('task', t3, t4, t5)
    p.add('event', e1, e2, e3, e4, e5)

    sp.add('task', t1, t2)

    e2.attach(sp)
    e3.attach(sp)
    e4.attach(sp)

    p.add('sequence', e1.add_link(sp, Task.OUT))
    p.add('sequence', sp.add_link(e5, Task.OUT))

    p.add('sequence', e2.add_link(t3, Task.OUT))
    p.add('sequence', e3.add_link(t4, Task.OUT))
    p.add('sequence', e4.add_link(t5, Task.OUT))

    # print(toPrettyXml(p.serialize()))
    # print(toPrettyXml(sp.serialize()))
    print(toPrettyXml(p.serialize()))
    # print(p.elements)
