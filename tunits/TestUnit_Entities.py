from models.entities.Container import Container
from models.entities.Entities import SeenMessage,SeenNotification, User, Notification, Invitation, Session, Project
from models.entities.Entities import *
from models.entities.enums.notificationtype import NotificationType 
import datetime

from sqlalchemy import or_,and_,func

# relationships Test


# def confirmtest():
#     user = Container.filter(User, User.firstName == 'Mohamed').first()
#     for relation in user.relations:
#         print(relation.userTwo.firstName)
#     for project in user.projects:
#         for shareLink in project.sharelinks:
#             print(shareLink.project.title)
#     for session in user.sessions:
#         print(session.project.title)
#     for history in user.histories:
#         print(history.project.title)
#     for message in user.messages:
#         print(message.session.title)
#     for notification in user.notifications:
#         print(notification.user.firstName)
#     for invitation in user.invitations:
#         print(invitation.recipient.firstName)
#     for invitationLink in user.invitationlinks:
#         print(invitationLink.session.title)
#     print(user.sparepwd.__class__.__name__)
#     user = Container.filter(User, User.firstName == 'Chakir').first()
#     print(user.sparepwd.verificationCode)


# # real situation test inserts
# def run():
#     user1 = User(firstName='Mohamed', email='Mohamed@123.com')
#     user2 = User(firstName='Ibrahim', email='Ibrahim@123.com')
#     user3 = User(firstName='Chakir', email='Chakir@123.com')
#     user4 = User(firstName='Hodaifa', email='Hodaifa@123.com')

#     relation1 = Relation(userOne=user1, userTwo=user2)
#     relation2 = Relation(userOne=user1, userTwo=user3)
#     relation3 = Relation(userOne=user1, userTwo=user4)

#     project = Project(title='database management', owner=user1)

#     session = Session(title='database management diagram making',
#                       owner=user1, project=project)

#     collab1 = Collaboration(user=user2, session=session, privilege='edit')
#     collab2 = Collaboration(user=user3, session=session, privilege='edit')

#     change1 = History(editor=user2, project=project,
#                       editDate=datetime.datetime.now())
#     change2 = History(editor=user2, project=project,
#                       editDate=datetime.datetime.now())
#     change3 = History(editor=user2, project=project,
#                       editDate=datetime.datetime.now())
#     change4 = History(editor=user3, project=project,
#                       editDate=datetime.datetime.now())

#     message1 = Message(user=user2, session=session, content='histury')
#     message2 = Message(user=user1, session=session, content='engiiiyn')

#     invitation = Invitation(sender=user1, recipient=user2, session=session)

#     invitationLink = InvitationLink(sender=user1, session=session)

#     shareLink = ShareLink(project=project)

#     sparepwd = SparePwd(user=user3, verificationCode='c18d45q4546s8')

#     Container.save(user2, user2, user3, user4, relation1, relation2, relation3,
#                    project, session, collab1, collab2, change1, change2, change3, change4, message1, message2, invitation, invitationLink, shareLink, sparepwd)

#     notification = Notification(actor=user2, invitationId=invitation.id)
#     Container.save(notification)

#     confirmtest()

def run():
    # Container.deleteObject(Container.filter(Project).first())
    user1 = User(firstName='Mohamed', lastName='El Kalai', userName='Mohamed123')
    user2 = User(firstName='Ibrahim', lastName='Areda', userName='Ibrahim123')
    user3 = User(firstName='Chakir', email='Chakir@123.com')
    user4 = User(firstName='Hodaifa', email='Hodaifa@123.com')

    project1 = Project(title='bpmntool', owner=user1)
    project2 = Project(title='bpmntool2', owner=user2)

    session1 = Session(title='bpmntoolsession', owner=user1, project=project1)
    session2 = Session(title='session2', owner=user2, project=project2)

    # collab1 = Collaboration(user=recipient, session=session, joiningDate=datetime.datetime.now(),privilege='edit')
    # collab2 = Collaboration(user=recipient2, session=session,joiningDate=datetime.datetime.now(), privilege='edit')
    # collab3 = Collaboration(user=recipient3, session=session2,joiningDate=datetime.datetime.now(), privilege='edit')

    # message1 = Message(user=recipient, session=session, sentDate=datetime.datetime.now(), content='message2')
    # message2 = Message(user=recipient2, session=session, sentDate=datetime.datetime.now(), content='message1')
    # message3 = Message(user=recipient2, session=session, sentDate=datetime.datetime.now(), content='message3')
    # message4 = Message(user=recipient2, session=session, sentDate=datetime.datetime.now(), content='message4')
    # message5 = Message(user=recipient3, session=session2, sentDate=datetime.datetime.now(), content='wrong')
    # message6 = Message(user=recipient3, session=session2, sentDate=datetime.datetime.now(), content='wrong2')
    # message7 = Message(user=sender, session=session2, sentDate=datetime.datetime.now(), content='i sent it in session2')
    # message8 = Message(user=sender, session=session, sentDate=datetime.datetime.now(), content='wrong i sent it')

    # invitation = Invitation(sender=sender, recipient=recipient,
    #                         session=session, privilege='edit')
     

    # invitationLink = InvitationLink(sender=sender, session=session, link='invlinkkkkkkkkkkkk')

    # shareLink = ShareLink(project=project, link='sharelinkkkkkkkkk')

    Container.save(user1,user2, user3, user4, project1, project2, session1, session2)#,invitation,invitationLink,shareLink,collab1,collab2,collab3,message1,message2,message3,message4,message5,message6,message7,message8)
    
    # notification = Notification(
    #     type=NotificationType.INVITED.value, nature='invitation', notificationTime='2020-07-01 10:46:38',recipient=recipient, actor=sender, invitationId=invitation.id)


    # notification2 = Notification(
    #     type=NotificationType.JOINED.value, nature='invitationLink',notificationTime='2020-07-02 11:34:00',recipient=invitationLink.sender, actor=recipient, invitationId=invitationLink.id)

    # notification3 = Notification(
    #     type=NotificationType.JOINED.value, nature='shareLink',notificationTime='2020-07-24 15:28:00',recipient=shareLink.project.owner, actor=recipient, invitationId=shareLink.id)
    
    # notification4 =Notification(
    #     type=NotificationType.ACCEPTED.value, nature='invitation',notificationTime='2020-07-24 15:28:00',recipient=invitation.sender, actor=recipient, invitationId=invitation.id)

    # notification5 =Notification(
    #     type=NotificationType.DECLINED.value, nature='invitation',notificationTime='2020-07-24 15:28:00',recipient=invitation.sender, actor=recipient, invitationId=invitation.id)

    # Container.save(notification,notification2,notification3,notification4,notification5)

    # seennotification = SeenNotification(notification=notification, seer=recipient)
    # seenmessage = SeenMessage(message=message1, seer=sender)
    # Container.save(seenmessage,seennotification)

    # invitation = Container.filter(Invitation).get(notification.invitationId)
    # print(f'notifcation recipient\'s name: {notification.recipient.firstName}')


    # user = Container.filter(User).get(48)

    # ### show last message in each session ( CURRENTUSER's one exclude - doesn't show session if he sent the last message there)
    # # messages = Container.filter(Message,Message.sessionId == Collaboration.sessionId,Message.userId != user.id,or_(Collaboration.userId == user.id, and_(Message.sessionId == Session.id, Session.ownerId == user.id) ),Message.sentDate.in_(Container.filter(func.max(Message.sentDate)).group_by(Message.sessionId))).group_by(Message.sessionId).all()
    
    # ### show last message for each session ( CURRENTUSER's one included ) / currently used
    # messages = Container.filter(Message,Message.sessionId == Collaboration.sessionId,or_(Collaboration.userId == user.id, and_(Message.sessionId == Session.id, Session.ownerId == user.id) ),Message.sentDate.in_(Container.filter(func.max(Message.sentDate)).group_by(Message.sessionId))).group_by(Message.sessionId).all(), 
    
    # for msg in messages:
    #     print(msg.content)






# The Cheated Testing Method
# def run():
#     for table in [vars(User),vars(SeenMessage),vars(SeenNotification), vars(Notification), vars(Invitation), vars(Session), vars(Project)]:
#         print('\n\n')
#         for att in table:
#             print(att)

