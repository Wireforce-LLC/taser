import os.path
import string

import plugins.source_map

PROMPT_TOOLKIT_ARGS = ""

def main(search_text=string.ascii_lowercase):
  files = plugins.source_map.main("read")
  out = []

  if isinstance(files, str):
    return files

  for file in files:
    line_count = 0

    with open(file, 'r') as file_:
      content = file_.readlines()
      file_.close()

    for line in content:
      line_count += 1

      if search_text.lower() in line.lower():
        out.append(
          f" {line_count:<6} | {os.path.basename(file):<26} | {line.strip()} "
        )


  return [""] + list(filter(lambda x: x, out)) + [""]
