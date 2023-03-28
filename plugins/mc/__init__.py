import os
import subprocess

from cp import get_cp
from libs import get_lib_link

PROMPT_TOOLKIT_ARGS = ""

def telnet():
  return "Some software is included in the Taser suite and only works on a local computer. " \
         "This programme is included in the Taser suite"

def main(path=""):
  subprocess.run(
    f"mc {path}",
    shell=True,
    cwd=os.path.abspath(get_cp())
  )
