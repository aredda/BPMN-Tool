from models.bpmn.Event import Event
from models.bpmn.Task import Task
from models.bpmn.Process import Process
from models.bpmn.enums.EventType import EventType
from models.bpmn.enums.EventDefinition import EventDefinition
from models.bpmn.enums.TaskType import TaskType
from models.bpmn.Gateway import Gateway
from helpers.StringHelper import toPrettyXml


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
              type=TaskType.SendMessage)
    t3 = Task(id='tsk3', name='Notification order rejected',
              type=TaskType.SendMessage)

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

    print(toPrettyXml(p.serialize()))
