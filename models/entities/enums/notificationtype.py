from enum import Enum

class NotificationType(Enum):
    INVITED = 'recievedInv' 
    ACCEPTED = 'acceptedInv'
    DECLINED = 'declinedInv'
    JOINED = 'joinedViaLink'