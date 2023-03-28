import xml.etree.ElementTree as ET

from sdk.require_android_path import require_android_strings_xml_path, require_android_themes_xml_path, \
  require_android_colors_xml_path


def get_themes(path: str = require_android_themes_xml_path()):
  tree = ET.parse(path)
  root = tree.getroot()

  d = {x.text: x.attrib['name'] for x in root.findall('string') if x.text}

  return d


def get_colors(path: str = require_android_colors_xml_path()):
  tree = ET.parse(path)
  root = tree.getroot()

  d = {}

  for x in root.findall('color'):
    d[x.attrib['name']] = x.text

  return d