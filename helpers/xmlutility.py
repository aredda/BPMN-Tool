import xml.etree.ElementTree as ET


def bytestoelement(bytesdata):
    return ET.fromstring(bytesdata)
