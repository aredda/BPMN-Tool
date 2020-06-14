from models.bpmn.artifact import Artifact
from helpers.stringhelper import camel_case
import xml.etree.ElementTree as et

class TextAnnotation(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)

    def serialize(self):
        # Create a Text Annotation
        e = et.Element('textAnnotation')
        e.attrib['id'] = self.id
        # Add a Text Element
        eText = et.Element('text')
        eText.text = self.name
        e.append(eText)
        # Return
        return e