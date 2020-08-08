import pickle as pk

from models.bpmn.bpmnelement import BPMNElement
from models.bpmn.container import Container

def display(container):
    if 'person' in container.elements:
        for e in container.elements['person']: print (e.id)
    else:
        print (f'{container.id} has no contained people')

c1 = Container(id='container1', name='Object Container')

e1 = BPMNElement(id='element1', name='Ibrahim Areda')
e2 = BPMNElement(id='element2', name='Joey Joestar')
e3 = BPMNElement(id='element3', name='Jotaro Kujoh')
e4 = BPMNElement(id='element4', name='Joseph Joestar')

c1.add('person', e1)
c1.add('person', e2)

serialized_data = pk.dumps(c1)

dc1: Container = pk.loads(serialized_data) 

print ('----- Deserialization 01:')
display(dc1)

c1.add('person', e3)

serialized_data = pk.dumps(c1)

dc2: Container = pk.loads(serialized_data)

print ('----- Deserialization 02:')
display(dc2)


