from models.bpmn.Artifact import Artifact

class Group(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)