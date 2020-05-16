import enum

class TaskType(enum.Enum):
    Default = 0
    User = 1
    Script = 2
    BusinessRule = 3
    Service = 4
    SendMessage = 5
    ReceiveMessage = 6