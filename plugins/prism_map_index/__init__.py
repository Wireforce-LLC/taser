import json
import os

import pandas as pd

import plugins.source_map

import plugins.impls_index
import plugins.source_creation_time
import plugins.tokenize
import plugins.detect_libs_stack
import plugins.ro2
import plugins.parse_layout
import plugins.unicorn_search
import plugins.revesiro
import plugins.fast_impl

import sdk.manifest
from cp import get_cp
from sdk import nav_graph
from sdk.build_gradle_parser import get_namespace
from sdk.layoutlib import analyze_xml
from sdk.layouts import get_list_layouts_path
from sdk.nav_graph import get_nav_graph_fragments
from sdk.require_android_path import require_android_colors_xml_path, require_android_strings_xml_path, \
  require_android_nav_graphs_path, require_android_package_by_root_path
from sdk.strings import get_strings
from sdk.theme import get_colors

PROMPT_TOOLKIT_ARGS = ""


def erase(data):
  return json.loads(json.dumps(data))

def main(dir=get_cp()):
  path_colors = require_android_colors_xml_path()
  path_strings = require_android_strings_xml_path()
  graphs_path = require_android_nav_graphs_path()

  source_map = plugins.source_map.main('index')
  source_creation_time = plugins.source_creation_time.main()
  tokenize = plugins.tokenize.main()
  libs_stack = plugins.detect_libs_stack.main()
  colors = {}
  strings = {}
  nav_graphs = []
  nav_graphs_fragments = {}
  layouts_xmls = get_list_layouts_path()

  if graphs_path:
    nav_graphs = nav_graph.get_nav_graphs(graphs_path)

    for graph in nav_graphs:
      if not os.path.isfile(graph):
        continue

      fragments = get_nav_graph_fragments(graph)

      nav_graphs_fragments[os.path.basename(graph)] = fragments


  if path_colors:
    colors = get_colors(path_colors)

  if path_strings:
    strings = get_strings(path_strings)

  fast_impls = plugins.fast_impl.main()

  activities = sdk.manifest.read_activities()
  permissions = sdk.manifest.read_permissions()

  ro2 = plugins.ro2.main(get_cp(), False)
  revesiro = plugins.revesiro.main(get_cp(), False)

  creation_start_at = min(source_creation_time.values())
  creation_end_at = max(source_creation_time.values())

  up_to_date_implementations = []

  layouts_warns = []

  for layout in layouts_xmls:
    layouts_warns.append({
      'layout': os.path.basename(layout),
      'warns': analyze_xml(layout)
    })

  for impl in fast_impls:
    result = plugins.unicorn_search.search(f"{impl.get('g', '')}:{impl.get('pkg', '')}")

    if result:
      up_to_date_implementations.append({
        'g': result['g'],
        'pkg': result['pkg'],
        'version': impl['version'],
        'latest_version': result['version'],
        'up_to_date': impl['version'] == result['version'],
      })

  up_to_date_implementations_map = list(map(lambda x: x['up_to_date'], up_to_date_implementations))

  if len(up_to_date_implementations_map) != 0:
    up_to_date_percent = up_to_date_implementations_map.count(True) / len(up_to_date_implementations_map)
  else:
    up_to_date_percent = 0

  revisoro_percent = 0
  
  if revesiro and 'warn_files' in revesiro.keys():
    revisoro_percent = (len(revesiro['warn_files']) / len(tokenize['files_tokens'])) * 100

  data: dict = {
    "namespace_app": get_namespace(),
    "source_map": source_map,
    "source_creation_time": source_creation_time,
    "fast_impls": fast_impls,
    "activities": activities,
    "permissions": permissions,
    "tokenize": tokenize,
    "colors_xml": colors,
    "strings_xml": strings,
    "creation_time_meta": {
      "start_at": creation_start_at,
      "end_at": creation_end_at,
      "elapsed_time": creation_end_at - creation_start_at,
      "elapsed_time_in_h": round((creation_end_at - creation_start_at) / 3600),
    },
    "nav_graphs": list(map(lambda x: os.path.basename(x), nav_graphs)) if nav_graph else [],
    "nav_graphs_fragments": nav_graphs_fragments,
    "libs_stack": libs_stack,
    "ro2": ro2,
    "revesiro": revesiro,
    "up_to_date_implementations": up_to_date_implementations,
    "up_to_date_percent": up_to_date_percent * 100,
    "revisoro_percent": revisoro_percent,
    "layouts_xmls": list(map(lambda x: os.path.basename(x), layouts_xmls)),
    "layoutlib_layouts_warns": list(filter(lambda x: x, layouts_warns))
  }

  globals()['__prism_map_index__'] = data

  return data
