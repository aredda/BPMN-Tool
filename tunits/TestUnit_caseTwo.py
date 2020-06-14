from models.bpmn.event import Event
from models.bpmn.task import Task
from models.bpmn.process import Process
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition
from models.bpmn.enums.tasktype import TaskType
from models.bpmn.gateway import Gateway
from helpers.stringhelper import to_pretty_xml


def run():

    # Instantiation Section

    p = Process(id='prc_1')

    e1 = Event(id='start', definition=EventDefinition.Default,
               type=EventType.Start, name='Complete Order')
    e2 = Event(id='rejected', definition=EventDefinition.Default,
               type=EventType.End, name='Rejected')
    e3 = Event(id='approved', definition=EventDefinition.Default,
               type=EventType.End, name='Approved')

    t1 = Task(id='tsk1', name='Approve Order', type=TaskType.User)
    t2 = Task(id='tsk2', name='Notification Order Approved',
              type=TaskType.Send)
    t3 = Task(id='tsk3', name='Notification order rejected',
              type=TaskType.Send)

    g = Gateway(id='gt1')

    # Flow/Link Section

    p.add('event', e1)
    p.add('event', e2)
    p.add('event', e3)

    p.add('task', t1)
    p.add('task', t2)
    p.add('task', t3)
    p.add('gateway', g)

    p.add('sequence', e1.add_link(t1, Task.OUT))
    p.add('sequence', t1.add_link(g, Task.OUT))
    p.add('sequence', g.add_link(t3, Task.OUT))
    p.add('sequence', g.add_link(t2, Task.OUT))
    p.add('sequence', t2.add_link(e3, Task.OUT))
    p.add('sequence', t3.add_link(e2, Task.OUT))

    print(to_pretty_xml(p.serialize()))
