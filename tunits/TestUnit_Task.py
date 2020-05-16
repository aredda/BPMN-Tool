from models.bpmn.Task import Task
from models.bpmn.enums.ActivityFlag import ActivityFlag
from models.bpmn.enums.TaskType import TaskType
from models.bpmn.Event import Event 
from models.bpmn.enums.EventDefinition import EventDefinition
from models.bpmn.enums.EventType import EventType
from helpers.StringHelper import toPrettyXml
import xml.etree.ElementTree as et

def run():
    t = Task(id='Receive Message', type=TaskType.User)
    e = Event(id='event_1', definition=EventDefinition.Message, type=EventType.Start)
    t1 = Task(id='Process Message',type=TaskType.Service)

    t.add_link(e)
    t.add_link(t1, Task.OUT)

    print (toPrettyXml(t.serialize()))
    print (toPrettyXml(e.serialize()))

    print (list(EventType))