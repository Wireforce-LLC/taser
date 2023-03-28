import glob
import os.path
import xml.etree.ElementTree as ET

from sdk.require_android_path import require_android_strings_xml_path, require_android_themes_xml_path, \
  require_android_colors_xml_path, require_android_nav_graphs_path


def get_nav_graphs(path: str = require_android_nav_graphs_path()):
  if path and os.path.isdir(path):
    return glob.glob(f"{path}/*.xml")

  return None


def get_nav_graph_fragments(path: str):
  tree = ET.parse(path)
  root = tree.getroot()

  fragments = []

  for x in root.findall('fragment'):
    fragments.append({
      "name": x.attrib.get('{http://schemas.android.com/apk/res/android}name', None),
      "label": x.attrib.get('{http://schemas.android.com/apk/res/android}label', None),
      "id": x.attrib.get('{http://schemas.android.com/apk/res/android}id', None),
      "layout": x.attrib.get('{http://schemas.android.com/tools}layout', None)
    })

  return fragments
