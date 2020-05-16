import enum

class ActivityFlag(enum.Enum):
    Default = 0
    Loop = 1
    Compensation = 2
    AdHoc = 3
    ParallelMultiple = 4
    SequentialMultiple = 5