import os.path

from prettytable import PrettyTable
from rich.table import Table

import plugins.detekt_report_to_dict
from sdk.manifest import read_activities
from sdk.require_android_path import require_android_manifest_path


def main(path: str):
  table = Table(show_lines=True, highlight=True)

  table.add_column("File", justify="left", no_wrap=True)
  table.add_column("Message")

  if not os.path.isfile(path):
    return "file doesnt exist"

  if path:
    files = plugins.detekt_report_to_dict.main(path)

    for file in files:
      for error in files[file]:
        pathname = os.path.basename(file)
        name = f"{pathname} [{error.get('line')}:{error.get('column')}]"

        table.add_row(
          name,
          error.get('message')
        )

    return table

  else:
    return f"path ({path}) is not a android dir"
