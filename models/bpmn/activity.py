from helpers.stringhelper import camel_case
from models.bpmn.linkable import Linkable
from models.bpmn.container import Container
from models.bpmn.enums.activityflag import ActivityFlag
from resources.namespaces import *

import xml.etree.ElementTree as et

class Activity(Linkable):

    def __init__(self, **args):
        Linkable.__init__(self, **args)

        self.flag = self.expects(args, 'flag', ActivityFlag.Default)

        self.ignore_attrs('flag')

    def serialize(self):
        e = Linkable.serialize(self)

        if self.flag in [ActivityFlag.ParallelMultiple, ActivityFlag.SequentialMultiple, ActivityFlag.Loop]:
            # instantiate characteristics element
            element = et.Element(bpmn + ('standard' if self.flag == ActivityFlag.Loop else 'multiInstance') + 'LoopCharacteristics')
            # mark as sequential
            if self.flag == ActivityFlag.SequentialMultiple: element.attrib['isSequential'] = 'true'
            # add characteristics element
            e.append(element)

        return e