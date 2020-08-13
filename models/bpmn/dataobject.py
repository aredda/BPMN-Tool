from models.bpmn.artifact import Artifact
from models.bpmn.dataobjectreference import DataObjectReference
from resources.namespaces import bpmn

class DataObject(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)

        self.reference = DataObjectReference(
            id=f'{self.id}_ref', dataObject=self)

    def serialize(self):
        original = Artifact.serialize(self)
        original.tag = bpmn + 'dataObject'
        original.attrib.pop('reference')
        return original

    def get_tag(self):
        return 'dataobject'