from models.bpmn.Process import Process
from models.bpmn.Task import Task
from models.bpmn.Lane import Lane
from helpers.StringHelper import toPrettyXml


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

    print(toPrettyXml(p.serialize()))
