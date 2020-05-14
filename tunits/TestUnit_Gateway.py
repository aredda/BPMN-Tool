from models.Gateway import Gateway
from models.enums.GatewayType import GatewayType
from helpers.StringHelper import toPrettyXml

def run():
    g = Gateway(type=GatewayType.Inclusive)

    for gt in list(GatewayType):
        print (toPrettyXml(Gateway(type=gt).serialize()))
    