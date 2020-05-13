from models.Linkable import Linkable
from models.Container import Container
from models.BPMNElement import BPMNElement
import xml.etree.ElementTree as et
import xml.dom.minidom as md
from models.enums.TaskType import TaskType

c = Container()

l1 = Linkable(id='Activity_1', name='Linkable 01')
l2 = Linkable(id='Gateway', name='Linkable 02')
l3 = Linkable(id='StartEvent_1', name='Linkable 03')

l1.add_link(l2)
l1.add_link(l3, Linkable.OUT)

c.add('linkables', l1)
c.add('linkables', l2)

#### Linkable Test Case
# print ('Incomings of L1')
# for link in l1.incoming:
#     print (link)
# print ('Outgoings of L2')
# for link in l2.outgoing:
#     print (link)

#### Container Test Case
# for link in c.elements['linkables']:
#     print(link)

#### Linkable Serialization Test Case
# e = l1.serialize()
# print (md.parseString(et.tostring(e)).toprettyxml())