from models.bpmn.flow import Flow


class Association(Flow):

    def __init__(self, **args):
        Flow.__init__(self, **args)
