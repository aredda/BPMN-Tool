from models.Artifact import Artifact

class DataObject(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)