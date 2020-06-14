
from helpers.modulefinder import getinstance
from helpers.stringhelper import getmodulename, getclassname


def run():
    # normal use
    obj = getinstance(classname='Gateway', folderpath=['models/bpmn'])
    print(type(obj))

    # dynamic use
    args = {'id': 101}
    obj2 = getinstance(classname=getclassname('exclusiveGateway'),
                       folderpath=['models/bpmndi', 'models/bpmn'], nameGetter=getmodulename, **args)
    print(obj2.id)
