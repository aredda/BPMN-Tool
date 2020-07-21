from enum import Enum


class NotificationNature(Enum):
    INV = 'invitation'
    INVLINK = 'invitationLink'
    SHARELINK = 'shareLink'
