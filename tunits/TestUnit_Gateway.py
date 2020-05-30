from models.bpmn.Gateway import Gateway
from models.bpmn.enums.GatewayType import GatewayType
from helpers.stringhelper import to_pretty_xml

def run():
    g = Gateway(type=GatewayType.Inclusive)

    for gt in list(GatewayType):
        print (to_pretty_xml(Gateway(type=gt).serialize()))