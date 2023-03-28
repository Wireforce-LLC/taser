import xml.etree.ElementTree as ET

from sdk.require_android_path import require_android_strings_xml_path


def get_strings(path: str = require_android_strings_xml_path()):
  tree = ET.parse(path)
  root = tree.getroot()

  d = {x.text: x.attrib['name'] for x in root.findall('string') if x.text}

  return d