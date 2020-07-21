import enum


class EventDefinition(enum.Enum):
    Default = 0
    Message = 1
    Escalation = 3
    Conditional = 4
    Link = 5
    Error = 6
    Cancel = 7
    Compensation = 8
    Signal = 9
    Multiple = 10
    ParallelMultiple = 11
    Terminate = 12
    Timer = 13
