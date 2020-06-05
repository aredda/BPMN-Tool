from models.bpmn.linkable import Linkable
import xml.etree.ElementTree as et
from models.bpmn.sequenceflow import SequenceFlow
from models.bpmn.messageflow import MessageFlow
from models.bpmn.association import Association
from models.bpmn.dataassociation import DataAssociation


def run_test():
    l = Linkable(id='whatever')
    print(et.tostring(l.serialize()))


def run_flow_test():
    l1 = Linkable(id='Activity_1', name='Linkable 01')
    l2 = Linkable(id='Gateway', name='Linkable 02')
    f = Association(id="id1", source=l1, target=l2)
    # f.serialize()
    print(et.tostring(f.serialize()))


def run_dataAssociation():
    l1 = Linkable(id='Activity_1', name='Linkable 01')
    l2 = Linkable(id='Gateway', name='Linkable 02')
    d = DataAssociation(id="haha", source=l1, target=l2, direction=0)
    print(et.tostring(d.serialize()))
