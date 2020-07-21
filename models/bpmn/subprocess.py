from resources.namespaces import bpmn
from models.bpmn.activity import Activity
from models.bpmn.enums.activityflag import ActivityFlag

class SubProcess(Activity):

    def __init__(self, **args):
        Activity.__init__(self, **args)

    def serialize(self):
        # retrieve the original serialized element
        e = Activity.serialize(self)
        # adhoc case 
        if self.flag == ActivityFlag.AdHoc:
            e.tag = bpmn + 'adHocSubProcss'

        return e
