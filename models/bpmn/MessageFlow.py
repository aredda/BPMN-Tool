import xml.etree.ElementTree as et

from models.bpmn.Flow import Flow


class MessageFlow(Flow):

    def __init__(self, **args):
        Flow.__init__(self, **args)