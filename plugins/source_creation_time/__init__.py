import os.path

import plugins.source_map

PROMPT_TOOLKIT_ARGS = ""

def main():
  files = plugins.source_map.main("read")
  times = {}

  if isinstance(files, str):
    return files

  for file in files:
    if os.path.isfile(file):
      times[os.path.basename(file)] = os.path.getctime(file)

  return times
