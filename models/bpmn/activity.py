from models.bpmn.linkable import Linkable
from models.bpmn.container import Container
from models.bpmn.enums.activityflag import ActivityFlag


class Activity(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.flag = self.expects(args, 'flag', ActivityFlag.Default)

        self.ignore_attrs('flag')
