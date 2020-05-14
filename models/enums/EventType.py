import enum

class EventType(enum.Enum):
    Start = 0
    IntermediateCatch = 1
    IntermediateThrow = 2
    End = 3
