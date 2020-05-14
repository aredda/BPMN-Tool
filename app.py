from models.Linkable import Linkable
from models.Container import Container
from models.BPMNElement import BPMNElement
import xml.etree.ElementTree as et
import xml.dom.minidom as md
from models.enums.TaskType import TaskType
from models.Lane import Lane
from models.Process import Process

c = Container()

l1 = Linkable(id='Activity_1', name='Linkable 01')
l2 = Linkable(id='Gateway', name='Linkable 02')
l3 = Linkable(id='StartEvent_1', name='Linkable 03')

l1.add_link(l2)
l1.add_link(l3, Linkable.OUT)

c.add('linkables', l1)
c.add('linkables', l2)


# Linkable Test Case
# print ('Incomings of L1')
# for link in l1.incoming:
#     print (link)
# print ('Outgoings of L2')
# for link in l2.outgoing:
#     print (link)

# Container Test Case
# for link in c.elements['linkables']:
#     print(link)

# Linkable Serialization Test Case
# e = l1.serialize()
# print (md.parseString(et.tostring(e)).toprettyxml())

lane1 = Lane(id="l1")
lane2 = Lane(id="l2")
lane3 = Lane(id="l3")

process = Process(id="p1")
process2 = Process(id="p2")

process.add('linkables', l1)
process.add('linkables', l2)
process.add('linkables', l3)

process2.add_lane(lane1)
process2.add_lane(lane2)


# lane serialization test
# ls = lane1.serialize()
# ls3 = lane3.serialize()
# print(et.tostring(ls))
# print(et.tostring(ls3))

# for lane in process2.lanes:
#       for element in lane1.elements["linkables"]:
#           print(element)

# for lane in process.lanes:
#     print(lane)

p = process.serialize()
print(md.parseString(et.tostring(p)).toprettyxml())
