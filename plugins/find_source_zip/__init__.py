import glob
import os
import time
from datetime import datetime

from pydash import sort_by

import plugins.source_map

PROMPT_TOOLKIT_ARGS = ""

def main(arg):
  files = glob.glob("./mount/sources/**/*")
  out = []

  for file in files:
    if arg.lower() in file.lower() and os.path.isdir(file):
      st_ctime = os.stat(file).st_ctime

      out.append({
        "st_ctime": st_ctime,
        "text": f"{str(time.strftime('%D %H:%M', time.localtime(st_ctime))):<15} | {file}"
      })

  return list(map(lambda x: x.get('text'), reversed(sort_by(out, "st_ctime"))))