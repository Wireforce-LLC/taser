from xml.dom import minidom

import pandas as pd
from pydash import uniq, flatten


def parse_xml(node):
  item = {}

  if node.nodeType == node.ELEMENT_NODE:
    if node.nodeName:
      item['tag'] = node.nodeName
      item['attrs'] = {}

      for a in node.attributes.keys():
        value = node.attributes[a].value

        if not value == {}:
          item['attrs'][a] = value

  if node.hasChildNodes():
    item['children'] = []
    for child in node.childNodes:
      parsed_child = parse_xml(child)

      if not parsed_child == {}:
        item['children'].append(parsed_child)

  return item


def parse_layout(filename: str):
  xmldoc = minidom.parse(filename)
  return parse_xml(xmldoc.documentElement)


def iterate_layout_into_2_deep_level(xml: dict, callback):
  # {
  #   'tag': 'androidx.constraintlayout.widget.ConstraintLayout',
  #   'attrs': {},
  #   'children': [
  #
  #   ]
  # }
  parent_element = {}

  for tag in xml:
    if tag == "tag":
      parent_element["tag"] = xml[tag]

    if tag == "attrs":
      parent_element["attrs"] = xml[tag]

    if tag == 'children':
      for children in xml[tag]:
        callback(parent_element, children)

        iterate_layout_into_2_deep_level(children, callback)


global_warns_list = []

def _check_constraint_sticky(node):
  warns = []

  if \
      not "app:layout_constraintBottom_toBottomOf" in node['attrs'].keys() \
          and not "app:layout_constraintBottom_toTopOf" in node['attrs'].keys() \
          and not "app:layout_constraintTop_toTopOf" in node['attrs'].keys() \
          and not "app:layout_constraintTop_toBottomOf" in node['attrs'].keys():
    warns.append({
      "level": "warning",
      "content": f"Element `{node['tag']}` is not attached to any of the Y-axis positions"
    })

  if \
      not "app:layout_constraintStart_toStartOf" in node['attrs'].keys() \
          and not "app:layout_constraintStart_toEndOf" in node['attrs'].keys() \
          and not "app:layout_constraintEnd_toStartOf" in node['attrs'].keys() \
          and not "app:layout_constraintEnd_toEndOf" in node['attrs'].keys():
    warns.append({
      "level": "warning",
      "content": f"Element `{node['tag']}` is not attached to any of the X-axis positions"
    })

  return warns

def _check_background_image_as_bg_attr(node):
  if "android:background" in node['attrs'].keys():
    if str(node['attrs']['android:background']).startswith('@drawable/') or \
     str(node['attrs']['android:background']).startswith('@minmap/'):
      return [
        {
          "level": "info",
          "content": f"Presumptive use of the image ({node['attrs']['android:background']}) in element {node['tag']} is detected"
        }
      ]

def _analyze_node(parent_node, node):
  global global_warns_list

  result = _check_constraint_sticky(node)

  if parent_node['tag'] == 'androidx.constraintlayout.widget.ConstraintLayout':
    global_warns_list.append(result)

  global_warns_list.append(_check_background_image_as_bg_attr(node))
  global_warns_list.append(_check_background_image_as_bg_attr(parent_node))

def analyze_xml(path: str):
  global global_warns_list

  global_warns_list = []

  xml = parse_layout(path)
  iterate_layout_into_2_deep_level(xml, _analyze_node)

  filtred = list(filter(lambda x: x, global_warns_list))

  filtered_global_warns_list = uniq(filtred)

  if not filtered_global_warns_list:
    return None

  return flatten(filtered_global_warns_list)