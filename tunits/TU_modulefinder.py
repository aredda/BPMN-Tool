
from helpers.modulefinder import getinstance, getclass
from helpers.stringhelper import getmodulename, getclassname


# getinstance test
# def run():
#     # normal use
#     obj = getinstance(classname='Gateway', folderpath=['models/bpmn'])
#     print(type(obj))

#     # dynamic use
#     args = {'id': 101}
#     obj2 = getinstance(classname=getclassname('exclusiveGateway'),
#                        folderpath=['models/bpmndi', 'models/bpmn'], nameGetter=getmodulename, **args)
#     print(obj2.id)


# getclass test
def run(tag: str):
    klass = getclass(classname=getclassname(tag), folderpath=[
                     'models/bpmn', 'models/bpmndi'], nameGetter=getmodulename)
    # c = klass(id=0, name='haha')
    print(klass)
