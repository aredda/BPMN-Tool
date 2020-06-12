import xml.etree.ElementTree as et

from helpers.deserializer import Deserializer, to_pretty_xml

d = Deserializer(et.parse('resources/xml/test.xml'))
d.prepare()
d.instantiate()

print (to_pretty_xml(d.definitions.serialize()))

exit (0)

for process_id in d.selements['process'].keys():
    print ('Process Id:', process_id)
    for breed in d.selements['process'][process_id]['children'].keys():
        print ('\tBreed:', breed)
        for e_id in d.selements['process'][process_id]['children'][breed].keys():
            print ('\t\t', d.selements['process'][process_id]['children'][breed][e_id])