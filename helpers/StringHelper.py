import xml.etree.ElementTree as et
import xml.dom.minidom as md

def camel_case(word: str):
    return word[0].lower() + word[1:]

def to_pretty_xml(element):
    return md.parseString(et.tostring(element)).toprettyxml()
    