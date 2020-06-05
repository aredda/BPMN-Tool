from models.bpmn.activity import Activity


class SubProcess(Activity):

    def __init__(self, **args):
        Activity.__init__(self, **args)
