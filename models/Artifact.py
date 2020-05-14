from models.BPMNElement import BPMNElement

class Artifact(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)