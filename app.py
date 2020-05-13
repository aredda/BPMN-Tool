from models.Linkable import Linkable
from models.Container import Container
from models.BPMNElement import BPMNElement

c = Container()

l1 = Linkable(id=1, name='Linkable 01')
l2 = Linkable(id=2, name='Linkable 02')

l1.add_link(l2)

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
for link in c.elements['linkables']:
    print(link)