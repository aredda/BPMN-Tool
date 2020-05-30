import xml.etree.ElementTree as et
import xml.dom.minidom as md

# BOOKMARK: engine connection string 
connection_string = 'mysql+pymysql://root:@localhost/bpmntool'

def camel_case(word: str):
    return word[0].lower() + word[1:]

def to_pretty_xml(element):
    return md.parseString(et.tostring(element)).toprettyxml()