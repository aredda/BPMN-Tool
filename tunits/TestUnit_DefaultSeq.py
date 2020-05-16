from models.bpmn.Task import Task
from models.bpmn.SequenceFlow import SequenceFlow
from helpers.StringHelper import toPrettyXml
from models.bpmn.enums.SequenceType import SequenceType
from models.bpmn.Activity import Activity
from models.bpmn.Linkable import Linkable
from models.bpmn.Container import Container

def run ():
    t1 = Task(id='t1', name='Testing Default Sequence')
    t2 = Task(id='t2', name='Displaying Results')

    # a = Linkable(name='yeah')
    # t1.add_link(t2, Task.IN)
    # print ('okay', toPrettyXml(a.serialize()))
    # t1.add_link(t2, Task.OUT)
    s = SequenceFlow(id='seqId', source=t1, target=t2, type=SequenceType.DEFAULT)

    link = t1.add_link(t2)

    print (toPrettyXml(s.serialize()))
    # print (toPrettyXml(t2.serialize()))
    print (toPrettyXml(link.serialize()))


