import json
import os

from prettytable import PrettyTable
from termcolor import colored

from core.cp import get_cp


def main():
  table = PrettyTable()
  table._max_width = {"Group": 32, "Id": 16, "Version": 17, "Last Ver.": 12, "up-to-date": 4}
  table.field_names = ["Group", "Id", "Version", "Last Ver.", "up-to-date"]

  table.align["Group"] = "l"
  table.align["Id"] = "l"
  table.align["Version"] = "l"
  table.align["Last Ver."] = "l"
  table.align["up-to-date"] = "l"

  table.padding_width = 2

  impls_map_file = get_cp() + '/implementations_map.json'

  if not os.path.isfile(impls_map_file):
    return "Implementations map not found. Try `impls_index()`"

  impls = open(impls_map_file, 'r').read()

  for impl in json.loads(impls):
    g = impl.get("g", "N/A")

    if impl.get("utd", None) == False:
      g = colored(g, 'red')
    elif impl.get("utd", None) == None:
      g = colored(g, 'yellow')
    elif impl.get("utd", None) == True:
      g = colored(g, 'green')

    table.add_row([
      g,
      impl.get("a", "N/A"),
      impl.get("v", "N/A"),
      impl.get("lv", "N/A"),
      impl.get("utd", "N/A"),
    ])

  return table
