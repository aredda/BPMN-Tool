from models.bpmn.artifact import Artifact

class DataStoreReference(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)