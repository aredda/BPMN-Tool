import xml.etree.ElementTree as et
import xml.dom.minidom as md

# BOOKMARK: engine connection string
database_name = 'bpmn-db'
server_path = 'mysql+pymysql://root:123@localhost/'
connection_string = server_path + database_name


def camel_case(word: str):
    return word[0].lower() + word[1:]


def to_pretty_xml(element):
    return md.parseString(et.tostring(element)).toprettyxml()


def getmodulename(classname: str):
    return classname[4:].lower() if classname.startswith('BPMN') and not classname.startswith('BPMNDI') else classname.lower()


def getclassname(tag: str):
    classname = (tag[0].upper()+tag[1:]
                 ) if not tag.lower().startswith('bpmn') else (tag[:5]).upper()+(tag[5:])

    if classname.lower().startswith('data') and classname.lower().endswith('association'):
        return 'DataAssociation'

    for name in ['Gateway', 'Event', 'Task', 'SubProcess', 'Activity']:
        if classname.lower().__contains__(name.lower()):
            return name

    for data in ['DataObjectReference', 'DataObject', 'DataStoreReference', 'TextAnnotation']:
        if classname.lower() == data.lower():
            return data

    if classname.lower().endswith('flow'):
        return 'SequenceFlow'

    return classname

def generate_code():
    import string, secrets
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))
