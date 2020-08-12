from models.entities.Container import Container
from models.entities.Entities import Invitation, Notification, InvitationLink, ShareLink
from models.entities.enums.notificationtype import NotificationType
from models.entities.enums.notificationnature import NotificationNature


def getNotificationContent(notification):
    if notification.type.endswith('Inv'):
        inv = Container.filter(Invitation).get(notification.invitationId)
        if notification.type == NotificationType.INVITED.value:
            return f'{inv.sender.userName} invited you to ({inv.session.title}) session.'
        elif notification.type == NotificationType.JOINED.value:
            return f'{inv.recipient.userName} joined ({inv.session.title}) session.'
        else:
            decision = 'accepted' if notification.type == NotificationType.ACCEPTED.value else 'declined'
            return f'{inv.recipient.userName} {decision} the ({inv.session.title}) session invitation.'
    else:
        if notification.nature == NotificationNature.INVLINK.value:
            invlink = Container.filter(InvitationLink).get(notification.invitationId)
            return f'{notification.actor.userName} joined ({invlink.session.title}) session via link.'
        elif notification.nature == NotificationNature.SHARELINK.value:
            sharelink = Container.filter(ShareLink).get(notification.invitationId)
            return f'{notification.actor.userName} joined ({sharelink.project.title}) project via link.'