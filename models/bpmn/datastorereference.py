from models.bpmn.artifact import Artifact
from resources.namespaces import bpmn

class DataStoreReference(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)
    
    def get_tag(self):
        return 'datastore'

    def serialize(self):
        e = super().serialize()
        e.tag = bpmn + 'dataStoreReference'
        return e