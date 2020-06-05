from models.bpmn.task import Task
from models.bpmn.sequenceflow import SequenceFlow
from helpers.stringhelper import to_pretty_xml
from models.bpmn.enums.sequencetype import SequenceType
from models.bpmn.activity import Activity
from models.bpmn.linkable import Linkable
from models.bpmn.container import Container

def run ():
    t1 = Task(id='t1', name='Testing Default Sequence')
    t2 = Task(id='t2', name='Displaying Results')

    # a = Linkable(name='yeah')
    # t1.add_link(t2, Task.IN)
    # print ('okay', to_pretty_xml(a.serialize()))
    # t1.add_link(t2, Task.OUT)
    s = SequenceFlow(id='seqId', source=t1, target=t2, type=SequenceType.DEFAULT)

    link = t1.add_link(t2)

    print (to_pretty_xml(s.serialize()))
    # print (to_pretty_xml(t2.serialize()))
    print (to_pretty_xml(link.serialize()))


