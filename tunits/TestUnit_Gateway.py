from models.bpmn.Gateway import Gateway
from models.bpmn.enums.GatewayType import GatewayType
from helpers.StringHelper import toPrettyXml

def run():
    g = Gateway(type=GatewayType.Inclusive)

    for gt in list(GatewayType):
        print (toPrettyXml(Gateway(type=gt).serialize()))