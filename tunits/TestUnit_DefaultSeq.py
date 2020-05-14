from models.Task import Task
from models.SequenceFlow import SequenceFlow
from helpers.StringHelper import toPrettyXml
from models.enums.SequenceType import SequenceType

def run ():
    t1 = Task(id='t1', name='Testing Default Sequence')
    t2 = Task(id='t2', name='Displaying Results')
    # t1.add_link(t2, Task.OUT)
    s = SequenceFlow(id='seqId',source=t1, target=t2, type=SequenceType.DEFAULT)

    # print (toPrettyXml(s.serialize()))
    print (toPrettyXml(t2.serialize()))


