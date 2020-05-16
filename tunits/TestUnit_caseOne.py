from models.bpmn.Event import Event
from models.bpmn.Task import Task
from models.bpmn.Process import Process
from models.bpmn.enums.EventType import EventType
from models.bpmn.enums.EventDefinition import EventDefinition
from helpers.StringHelper import toPrettyXml


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

    print(toPrettyXml(process.serialize()))
