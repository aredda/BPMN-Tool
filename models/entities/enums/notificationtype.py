from enum import Enum

class NotificationType(Enum):
    INVITED = 'receivedInv'
    ACCEPTED = 'acceptedInv'
    DECLINED = 'declinedInv'
    JOINED = 'joinedViaLink'