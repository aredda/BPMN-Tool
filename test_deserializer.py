import xml.etree.ElementTree as et

from helpers.deserializer import Deserializer, to_pretty_xml

d = Deserializer(et.parse('resources/xml/subprocess.xml'))

print (to_pretty_xml(d.definitions.serialize()))