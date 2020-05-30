from models.bpmn.Process import Process
from models.bpmn.Task import Task
from models.bpmn.enums.TaskType import TaskType
from models.bpmn.DataObject import DataObject
from models.bpmn.DataAssociation import DataAssociation
from models.bpmn.enums.DataAssocDirection import DataAssocDirection
from models.bpmn.DataObjectReference import DataObjectReference
from helpers.stringhelper import to_pretty_xml
from models.bpmn.DataSotreReference import DataStoreReference
from models.bpmn.Event import Event
from models.bpmn.enums.EventDefinition import EventDefinition
from models.bpmn.enums.EventType import EventType


def run():

    process = Process(id='prc1', name='Main Participant')

    task1 = Task(id='tsk1', name='Connect to data object')
    task2 = Task(id='tsk2', name='Do Another Thing')

    start_event = Event(
        definition=EventDefinition.Escalation, type=EventType.Start)

    dtObj1 = DataObject(id='dtObj1', name='whatEverDtObj')
    dtStore = DataStoreReference(id='dtStore1', name='Database')

    # the direction of this assoc is IN in default
    task1.link_data(dtObj1, DataAssocDirection.IN)
    start_event.link_data(dtStore, DataAssocDirection.IN)

    print(to_pretty_xml(task1.serialize()))
    print(to_pretty_xml(dtObj1.serialize()))
    print(to_pretty_xml(dtObj1.reference.serialize()))
