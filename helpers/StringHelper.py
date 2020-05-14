import xml.etree.ElementTree as et
import xml.dom.minidom as md

def camelCase(word: str):
    return word[0].lower() + word[1:]

def toPrettyXml(element):
    return md.parseString(et.tostring(element)).toprettyxml()
    