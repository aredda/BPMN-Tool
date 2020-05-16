from models.bpmn.Artifact import Artifact
from models.bpmn.DataObjectReference import DataObjectReference


class DataObject(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)

        self.reference = DataObjectReference(
            id=f'{self.id}_ref', dataObject=self)

    def serialize(self):
        original = Artifact.serialize(self)
        original.attrib.pop('reference')
        return original
