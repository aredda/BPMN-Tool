from models.Process import Process
from models.Task import Task
from models.enums.TaskType import TaskType
from models.DataObject import DataObject
from models.DataAssociation import DataAssociation
from models.enums.DataAssocDirection import DataAssocDirection
from models.DataObjectReference import DataObjectReference
from helpers.StringHelper import toPrettyXml
from models.DataSotreReference import DataStoreReference
from models.Event import Event
from models.enums.EventDefinition import EventDefinition
from models.enums.EventType import EventType

def run():
    
    process = Process(id='prc1', name='Main Participant')

    task1 = Task(id='tsk1', name='Connect to data object')
    task2 = Task(id='tsk2', name='Do Another Thing')
    
    start_event = Event(definition=EventDefinition.Escalation, type=EventType.Start);

    dtObj1 = DataObject(id='dtObj1', name='whatEverDtObj')
    dtStore = DataStoreReference(id='dtStore1', name='Database')

    # the direction of this assoc is IN in default
    task1.link_data(dtStore, DataAssocDirection.IN)
    start_event.link_data(dtStore, DataAssocDirection.IN)

    print (toPrettyXml(start_event.serialize()))
