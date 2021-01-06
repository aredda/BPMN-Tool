from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from helpers.stringhelper import connection_string, server_path, database_name
from helpers.filehelper import filetobytes
from sqlalchemy.exc import InternalError

class Container():

    metaData = None
    scopedSession = None
    session = None
    Base = None

    configured = False
    relationshipsConfigured = False

    threadSession = None

    @staticmethod
    def configure():
        Container.Base = declarative_base()
        # Creating the engine that holds the connection to the database
        engine = Container.connect()
        # Creating metaData that holds our Tables and their associations
        Container.metaData = MetaData(bind=engine)
        # Creating a session that holds all our objects and which takes care of communicating queries to our database
        Session = sessionmaker(bind=engine, autocommit=True, autoflush= False, expire_on_commit= False)
        Container.session = Session()
        Container.threadSession = Session()
        # Container.scopedSession = scoped_session(sessionmaker(bind=engine))
        Container.configured = True
        # check if tables are created
        table_count_result = Container.session.execute("SELECT count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '" + database_name + "'")
        table_count = int(table_count_result.first()[0])
        if table_count == 0:
            Container.loadSchema()

    @staticmethod
    def connect():
        # request a connection
        engine = create_engine(connection_string)
        # try to connect to the database
        engine.connect()
        # return the engine
        return engine

    @staticmethod
    def configureRelationships(relationships):
        for relation in relationships:
            Container.configureRelationship(relation[0], relation[1], relation[2],
                                            relation[3], False if len(relation) < 5 else True)
        Container.relationshipConfigured = True

    @staticmethod
    def configureRelationship(childModel, parentModel, propertyName, foreignkey, isOnetoOne):
        # Get childModel and parentModel names
        parentModelName: str = parentModel().__class__.__name__
        childModelName: str = childModel().__class__.__name__

        # get parent's child's property name
        propName = childModelName.lower()
        if propName[-1] == 'y':
            propName = propName.replace('y', 'ie')
        propName += 's'

        # Create the child relationship
        childRelation = relationship(
            parentModelName, foreign_keys=f'[{childModelName}.{foreignkey}]',backref= backref(propName, uselist=True, cascade="all,delete") if hasattr(parentModel, propName) == False else None)

        if isOnetoOne == True:
            # we use set useList = False in both parent and child to show that it's a O2O relationship
            childRelation.uselist = False
            childRelation.backref = backref(propName, uselist=False, cascade="all,delete")

        # set the childrelation to childModel
        setattr(childModel, propertyName, childRelation)

    @staticmethod  # used for add and update
    def save(*objs):
        Container.session.add_all(objs)
        Container.session.flush()

    @staticmethod
    def deleteObject(obj):
        Container.session.delete(obj)
        Container.session.flush()

    @staticmethod
    def filter(modelType, *conditions):
        return Container.session.query(modelType).filter(*conditions)

    @staticmethod
    def threadSafeFilter(modelType, *conditions):
        Container.threadSession.flush()
        return Container.threadSession.query(modelType).filter(*conditions)
    
    @staticmethod
    def loadSchema():
        # request connection to the created database
        engine = create_engine(connection_string)
        # get tables creation code
        sql = (filetobytes('resources/database.sql')).decode('utf-8')
        # loop on the statements and execute each one
        for st in sql.replace('\\n', '').replace('\\r', '').split(';'):
            try:
                engine.execute(st)
            except:
                continue

if Container.configured == False:
    Container.configure()
