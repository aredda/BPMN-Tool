from models.Container import Container
# from models.Activity import Activity


class SubProcess(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

    def serialize(self):
        pass
