from helpers.StringHelper import camelCase
from models.Activity import Activity
from models.enums.TaskType import TaskType
import xml.etree.ElementTree as et


class Task(Activity):

    def __init__(self, **args):
        Activity.__init__(self, **args)

        self.type: TaskType = self.expects(args, 'type', TaskType.Default)

        self.ignore_attrs('type')

    def serialize(self):
        taskElement = Activity.serialize(self)
        taskElement.tag = 'task' if self.type == TaskType.Default else camelCase(
            self.type.name) + 'Task'
        return taskElement
