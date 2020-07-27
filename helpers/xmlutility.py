import xml.etree.ElementTree as ET

def savexml(filename: str, xmlstring: str):
    with open(filename, 'w') as file:
        file.write(xmlstring)

def bytestoelement(bytesdata):
    return ET.fromstring(bytesdata)

def elementtobytes(element):
    return ET.tostring(element)