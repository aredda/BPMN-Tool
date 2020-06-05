from models.bpmn.event import Event
from models.bpmn.task import Task
from models.bpmn.process import Process
from models.bpmn.enums.eventtype import EventType
from models.bpmn.enums.eventdefinition import EventDefinition
from helpers.stringhelper import to_pretty_xml


def run():

    process = Process(id="proc", name='Participant')

    task = Task(id="mainTask", name="eat chinese food")

    startEvent = Event(id="start", type=EventType.Start,
                       definition=EventDefinition.Default)

    endEvent = Event(id="end", type=EventType.End,
                     definition=EventDefinition.Default)

    process.add('sequence', startEvent.add_link(task, Task.OUT))
    process.add('sequence', task.add_link(endEvent, Task.OUT))
    process.add('task', task)
    process.add('event', startEvent)
    process.add('event', endEvent)

    print(to_pretty_xml(process.serialize()))
