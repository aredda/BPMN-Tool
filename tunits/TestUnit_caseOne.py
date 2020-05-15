from models.Event import Event
from models.Task import Task
from models.Process import Process
from models.enums.EventType import EventType
from models.enums.EventDefinition import EventDefinition
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
