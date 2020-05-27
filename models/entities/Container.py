from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


class Container():

    metaData = None
    session = None
    Base = None

    configured = False
    relationshipsConfigured = False

    @staticmethod
    def configure():
        Container.Base = declarative_base()
        # Creating the engine that holds the connection to the database
        engine = create_engine('mysql://root:@localhost/bpmntool')
        # Creating metaData that holds our Tables and their associations
        Container.metaData = MetaData(bind=engine)
        # Creating a session that holds all our objects and which takes care of communicating queries to our database
        Session = sessionmaker(bind=engine)
        Container.session = Session()

        Container.configured = True

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

        # Create the child relationship
        childRelation = relationship(
            parentModelName, foreign_keys=f'[{childModelName}.{foreignkey}]')

        # get parent's child's property name
        propName = childModelName.lower()
        if isOnetoOne == True:
            # we use set useList = False in both parent and child to show that it's a O2O relationship
            childRelation.uselist = False
            childRelation.backref = backref(propName, uselist=False)
        else:
            # if it's not O2O then we add a relationship on the parent side , which will be a list of children
            # we set up the parent's child's property according to the childModel name
            if propName[-1] == 'y':
                propName = propName.replace('y', 'ie')
            propName += 's'
            # check if the Model doesn't have a list of childModel given
            if hasattr(parentModel, propName) == False:
                # Create parent relationship
                parentRelation = relationship(
                    childModelName, primaryjoin=f'{parentModelName}.id == {childModelName}.{foreignkey}')
                # set the parentrelation to the parentModel
                setattr(parentModel, propName, parentRelation)

        # set the childrelation to childModel
        setattr(childModel, propertyName, childRelation)

    @staticmethod
    def update(Class, id, **args):
        obj = Container.filter(Class).get(id)
        for key, value in args.items():
            setattr(obj, key, value)
        Container.saveObject(obj)
        return obj

    @staticmethod
    def delete(Class, id):
        obj = Container.filter(Class).get(id)
        Container.deleteObject(obj)

    @staticmethod
    def add(Class, **args):
        obj = Class()
        for key, value in args.items():
            setattr(obj, key, value)
        Container.saveObject(obj)
        return obj

    @staticmethod  # used for add and update
    def save(*objs):
        Container.session.add_all(objs)
        Container.session.commit()

    @staticmethod
    def deleteObject(obj):
        Container.session.delete(obj)
        Container.session.commit()

    @staticmethod
    def filter(modelType, *conditions):
        return Container.session.query(modelType).filter(*conditions)


if Container.configured == False:
    Container.configure()
