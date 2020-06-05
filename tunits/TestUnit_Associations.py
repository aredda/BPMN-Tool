from models.bpmn.process import Process
from models.bpmn.task import Task
from models.bpmn.enums.tasktype import TaskType
from models.bpmn.dataobject import DataObject
from models.bpmn.dataassociation import DataAssociation
from models.bpmn.enums.dataassocdirection import DataAssocDirection
from models.bpmn.dataobjectreference import DataObjectReference
from helpers.stringhelper import to_pretty_xml
from models.bpmn.datastorereference import DataStoreReference
from models.bpmn.event import Event
from models.bpmn.enums.eventdefinition import EventDefinition
from models.bpmn.enums.eventtype import EventType


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
