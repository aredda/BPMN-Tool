from models.entities.Container import Container
from models.entities.Entities import *
import datetime


# real situation test inserts
'''
def run():
    user1 = User(firstName='Mohamed', email='Mohamed@123.com')
    user2 = User(firstName='Ibrahim', email='Ibrahim@123.com')
    user3 = User(firstName='Chakir', email='Chakir@123.com')
    user4 = User(firstName='Hodaifa', email='Hodaifa@123.com')

    relation1 = Relation(userOne=user1, userTwo=user2)
    relation2 = Relation(userOne=user1, userTwo=user3)
    relation3 = Relation(userOne=user1, userTwo=user4)

    project = Project(title='database management', owner=user1)

    session = Session(title='database management diagram making',
                      owner=user1, project=project)

    collab1 = Collaboration(user=user2, session=session, privilege='edit')
    collab2 = Collaboration(user=user3, session=session, privilege='edit')

    change1 = History(editor=user2, project=project,
                      editDate=datetime.datetime.now())
    change2 = History(editor=user2, project=project,
                      editDate=datetime.datetime.now())
    change3 = History(editor=user2, project=project,
                      editDate=datetime.datetime.now())
    change4 = History(editor=user3, project=project,
                      editDate=datetime.datetime.now())

    message1 = Message(user=user2, session=session, content='histury')
    message2 = Message(user=user1, session=session, content='engiiiyn')

    invitation = Invitation(sender=user1, recipient=user2, session=session)

    notification = Notification(actor=user2, invitationId=invitation.id)

    invitationLink = InvitationLink(sender=user1, session=session)

    shareLink = ShareLink(project=project)

    sparepwd = SparePwd(user=user3)

    Container.save(user2, user2, user3, user4, relation1, relation2, relation3,
                   project, session, collab1, collab2, change1, change2, change3, change4, message1, message2, invitation, invitationLink, notification, shareLink, sparepwd)
'''


# relationships Test

def run():
    user = Container.filter(User, User.firstName == 'Mohamed').first()
    for relation in user.relations:
        print(relation.userTwo.firstName)
    for project in user.projects:
        for shareLink in project.sharelinks:
            print(shareLink.project.title)
    for session in user.sessions:
        print(session.project.title)
    for history in user.histories:
        print(history.project.title)
    for message in user.messages:
        print(message.session.title)
    for notification in user.notifications:
        print(notification.user.firstName)
    for invitation in user.invitations:
        print(invitation.recipient.firstName)
    for invitationLink in user.invitationlinks:
        print(invitationLink.session.title)
    print(user.sparepwd.__class__.__name__)
    user = Container.filter(User, User.firstName == 'Mohamed').first()
    print(user.sparepwd.verificationCode)


'''


# The Cheated Testing Method
def run():
    for att in vars(User):
        print(att)
'''
