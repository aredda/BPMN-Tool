from models.bpmn.process import Process
from models.bpmn.task import Task
from models.bpmn.lane import Lane
from helpers.stringhelper import to_pretty_xml


def run():
    p = Process(id='prc_1', name='Participant 01')

    l1 = Lane(id='ln_1', name='Areda', process=p)
    l2 = Lane(id='ln_2', name='Areda', process=p)

    t1 = Task(id='tsk_1', name='Do something 1')
    t2 = Task(id='tsk_2', name='Do something 2')
    t3 = Task(id='tsk_3', name='Do something 3')

    l1.add('task', t1)
    l2.add('task', t2)
    l1.add('task', t3)

    print(to_pretty_xml(p.serialize()))
