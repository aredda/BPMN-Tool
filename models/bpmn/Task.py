from helpers.stringhelper import camel_case
from models.bpmn.Activity import Activity
from models.bpmn.enums.TaskType import TaskType
import xml.etree.ElementTree as et


class Task(Activity):

    def __init__(self, **args):
        Activity.__init__(self, **args)

        self.type: TaskType = self.expects(args, 'type', TaskType.Default)

        self.ignore_attrs('type')

    def serialize(self):
        taskElement = Activity.serialize(self)
        taskElement.tag = 'task' if self.type == TaskType.Default else camel_case(
            self.type.name) + 'Task'
        return taskElement
