import xml.etree.ElementTree as et

from models.bpmn.TextAnnotation import TextAnnotation
from models.bpmn.Group import Group
from models.bpmn.DataObject import DataObject
from models.bpmn.DataSotreReference import DataStoreReference
from helpers.stringhelper import to_pretty_xml

def run():
    annot = TextAnnotation(id='textAnnot1', name='This is an annotation')
    grp = Group(id='grp1', name='A group')
    obj = DataObject(id='dtObj1')
    ref = DataStoreReference(id='dtRef1')

    print (to_pretty_xml(annot.serialize()))
    print (to_pretty_xml(grp.serialize()))
    print (to_pretty_xml(obj.serialize()))
    print (to_pretty_xml(ref.serialize()))