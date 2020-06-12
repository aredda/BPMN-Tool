import xml.etree.ElementTree as et
import xml.dom.minidom as md

# BOOKMARK: engine connection string
connection_string = 'mysql+pymysql://root:@localhost/bpmntool'


def camel_case(word: str):
    return word[0].lower() + word[1:]


def to_pretty_xml(element):
    return md.parseString(et.tostring(element)).toprettyxml()


def getmodulename(classname: str):
    return classname[4:].lower() if classname.startswith('BPMN') and not classname.startswith('BPMNDI') else classname.lower()


def getclassname(tag: str):
    classname = (tag[0].upper()+tag[1:]) if not tag.startswith('BPMN') else tag

    if classname.startswith('Data') and classname.endswith('Association'):
        classname = 'DataAssociation'

    for name in ['Gateway', 'Event', 'Task', 'SubProcess', 'Activity']:
        if classname.__contains__(name):
            classname = name

    return classname
