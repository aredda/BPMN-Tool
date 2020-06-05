from models.bpmn.artifact import Artifact

class Group(Artifact):

    def __init__(self, **args):
        Artifact.__init__(self, **args)