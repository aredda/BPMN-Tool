from sqlalchemy import Table
from models.entities.Container import Container

Base = Container.Base
metaData = Container.metaData

# USER SECTION
class User(Base):
    __table__ = Table('users', metaData, autoload=True)

class Relation(Base):
    __table__ = Table('relations', metaData, autoload=True)

# COLLABORATION SECTION
class Project(Base):
    __table__ = Table('projects', metaData, autoload=True)

class Session(Base):
    __table__ = Table('sessions', metaData, autoload=True)

class Collaboration(Base):
    __table__ = Table('collaborations', metaData, autoload=True)

class History(Base):
    __table__ = Table('history', metaData, autoload=True)

# MESSAGE SECTION
class Message(Base):
    __table__ = Table('messages', metaData, autoload=True)

# NOTIFICATION & INVITATION SECTION
class Notification(Base):
    __table__ = Table('notifications', metaData, autoload=True)

class Invitation(Base):
    __table__ = Table('invitations', metaData, autoload=True)

class InvitationLink(Base):
    __table__ = Table('invitationLinks', metaData, autoload=True)

class ShareLink(Base):
    __table__ = Table('shareLinks', metaData, autoload=True)

# SPARE PASSWORD
class SparePwd(Base):
    __table__ = Table('sparePwd', metaData, autoload=True)

# RELATIONSHIPS
relationships = [
    [Relation, User, 'userOne', 'userOneId'],
    [Relation, User, 'userTwo', 'userTwoId'],
    [Project, User, 'owner', 'ownerId'],
    [Session, User, 'owner', 'ownerId'],
    [Session, Project, 'project', 'projectId'],
    [Collaboration, User, 'user', 'userId'],
    [Collaboration, Session, 'session', 'sessionId'],
    [History, User, 'editor', 'editorId'],
    [History, Project, 'project', 'projectId'],
    [Message, User, 'user', 'userId'],
    [Message, Session, 'session', 'sessionId'],
    [Notification, User, 'actor', 'actorId'],
    [Invitation, User, 'sender', 'senderId'],
    [Invitation, User, 'recipient', 'recipientId'],
    [Invitation, Session, 'session', 'sessionId'],
    [InvitationLink, User, 'sender', 'senderId'],
    [InvitationLink, Session, 'session', 'sessionId'],
    [ShareLink, Project, 'project', 'projectId'],
    [SparePwd, User, 'user', 'userId', True]
]

if Container.relationshipsConfigured == False:
    Container.configureRelationships(relationships)
