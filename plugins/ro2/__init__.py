import os
import string
import subprocess

from cp import get_cp
from libs import get_lib_link
from sdk import is_android_dir

PROMPT_TOOLKIT_ARGS = ""

ro2_lib_path = get_lib_link('ro2')

def main(path=get_cp(), inShell=True):
  if not ro2_lib_path:
    return "ro2 not selected in libs.yml"

  if not is_android_dir:
    return "ro2 work only inside android dir"

  if inShell:
    out = subprocess.run(
      f"java -jar {ro2_lib_path} --treeDiff --path {os.path.abspath(path)}",
      shell=True,
      cwd=os.path.abspath("./mount/ro2")
    )

  else:
    with open(os.devnull, 'w+') as devnull:
      out = subprocess.run(
        f"java -jar {ro2_lib_path} --treeDiff --path {os.path.abspath(path)}",
        cwd=os.path.abspath("./mount/ro2"),
        shell=True,
        capture_output=True,
        text=True
      )

    if out.stdout:
      sources = {}

      if not "root/" in out.stdout:
        return {}

      root_source = None
      children_source = None

      for line in out.stdout.split("\n"):
        if line.startswith("├─"):
          root_source = line.replace('├─', '').strip()
          sources[root_source] = {}

        if line.startswith("│  ├─"):
          children_source = line.replace('│  ├─', '').strip()

          sources[root_source][children_source] = {}

        if line.startswith("│  │  ├─"):
          relation_source = line.replace('│  │  ├─', '').strip().split(" ")[0]
          relation_size = int(
            line
            .replace('│  │  ├─', '')
            .strip()
            .split(" ")[1]
            .strip(string.ascii_letters)
            .replace('(', '')
            .replace(')', '')
          )

          sources[root_source][children_source][relation_source] = relation_size

      return sources