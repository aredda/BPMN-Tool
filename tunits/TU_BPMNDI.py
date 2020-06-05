from models.bpmndi.bpmndielement import BPMNDIElement
from models.bpmndi.label import BPMNLabel
from models.bpmndi.bounds import Bounds
from models.bpmn.task import Task
from helpers.stringhelper import to_pretty_xml
from models.bpmndi.shape import BPMNShape
from models.bpmndi.edge import BPMNEdge
from models.bpmndi.plane import BPMNPlane

def run():

    e = BPMNDIElement(id='di_e', element=Task(id='tsk1', name='TASK'))
    lbl = BPMNLabel(bounds=Bounds((10, 20), (100, 25)))

    shape = BPMNShape(bounds=Bounds((15,13),(12,13)), label=lbl)

    edge = BPMNEdge(id='edge_id',start=(15,15), end=(30,12), label=lbl)

    plane = BPMNPlane(element=edge)
    plane.add('edge', edge)
    plane.add('shape', shape)


    print (to_pretty_xml(plane.serialize()))
