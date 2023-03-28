import os.path

from sdk import layoutlib

PROMPT_TOOLKIT_ARGS = ""

def main(layout: str):
  if not os.path.isfile(layout):
    return None

  return layoutlib.parse_layout(layout)