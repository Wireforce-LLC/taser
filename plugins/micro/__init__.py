import os
import subprocess

from cp import get_cp
from libs import get_lib_link

PROMPT_TOOLKIT_ARGS = ""

micro_lib_path = get_lib_link('micro')

def telnet():
  return "Some software is included in the Taser suite and only works on a local computer. " \
         "This programme is included in the Taser suite"


def main(path=""):
  if not micro_lib_path:
    return "micro not selected in libs.yml"

  subprocess.run(
    f"{micro_lib_path} {path}",
    shell=True,
    cwd=os.path.abspath(get_cp())
  )
