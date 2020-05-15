from models.Linkable import Linkable
from models.Container import Container
from models.enums.ActivityFlag import ActivityFlag


class Activity(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.flag = self.expects(args, 'flag', ActivityFlag.Default)

        self.ignore_attrs('flag')
