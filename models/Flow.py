from models.BPMNElement import BPMNElement


class Flow(BPMNElement):

    def __init__(self, **args):
        BPMNElement.__init__(self, **args)

        self.source = self.expects(args, "source")
        self.target = self.expects(args, "target")

    def serialize(self):
        pass
