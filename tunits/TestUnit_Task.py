from models.bpmn.task import Task
from models.bpmn.enums.activityflag import ActivityFlag
from models.bpmn.enums.tasktype import TaskType
from models.bpmn.event import Event 
from models.bpmn.enums.eventdefinition import EventDefinition
from models.bpmn.enums.eventtype import EventType
from helpers.stringhelper import to_pretty_xml
import xml.etree.ElementTree as et

def run():
    t = Task(id='Receive Message', type=TaskType.User)
    e = Event(id='event_1', definition=EventDefinition.Message, type=EventType.Start)
    t1 = Task(id='Process Message',type=TaskType.Service)

    t.add_link(e)
    t.add_link(t1, Task.OUT)

    print (to_pretty_xml(t.serialize()))
    print (to_pretty_xml(e.serialize()))

    print (list(EventType))