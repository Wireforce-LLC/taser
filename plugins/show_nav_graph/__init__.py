import os.path

from prettytable import PrettyTable

from sdk import nav_graph
from sdk.nav_graph import get_nav_graph_fragments
from sdk.require_android_path import require_android_nav_graphs_path


def main():
  table = PrettyTable()
  table._max_width = {"Graph": 20, "Fragment (Label)": 25, "Class": 42, "ID": 40}
  table.field_names = ["Graph", "Fragment (Label)", "Class", "ID"]
  table.align["Graph"] = "l"
  table.align["Fragment (Label)"] = "l"
  table.align["Class"] = "l"
  table.align["ID"] = "l"
  table.padding_width = 2

  graphs_path = require_android_nav_graphs_path()
  graphs = nav_graph.get_nav_graphs(graphs_path)

  for graph in graphs:
    if not os.path.isfile(graph):
      continue

    fragments = get_nav_graph_fragments(graph)

    for fragment in fragments:
      table.add_row([
        os.path.basename(graph),
        fragment.get("label", "N/A"),
        fragment.get("name", "N/A"),
        fragment.get("id", "N/A"),
      ])

  return table