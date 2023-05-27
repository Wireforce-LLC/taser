import os
import string
import subprocess

from cp import get_cp
from libs import get_lib_link
from sdk import is_android_dir

PROMPT_TOOLKIT_ARGS = ""

revisoro_lib_path = get_lib_link('revisoro')

def main(path=get_cp(), inShell=True):
  if not revisoro_lib_path:
    return "revisoro not selected in libs.yml"

  if not is_android_dir:
    return "revisoro work only inside android dir"

  if inShell:
    out = subprocess.run(
      f"java -jar {revisoro_lib_path} {os.path.abspath(path)}",
      shell=True,
      cwd=os.path.abspath("./mount/revisoro")
    )

  else:
    with open(os.devnull, 'w+') as devnull:
      out = subprocess.run(
        f"java -jar {revisoro_lib_path} {os.path.abspath(path)}",
        cwd=os.path.abspath("./mount/revisoro"),
        shell=True,
        capture_output=True,
        text=True
      )

      source = {
        "package_name": None,
        "warn_files": []
      }

      if out.stdout:
        for line in out.stdout.strip().split("\n"):
          command = line.split('/')

          if command[0].startswith("pgName:"):
            source['package_name'] = command[0].replace("pgName:", "")

          if command[0] == "@":
            file_name = command[1].replace("file:", '')
            package_name = command[2].replace("package:", '')
            percent_match = float(command[3].replace("percentMatch:", ''))

            if file_name in ["Shape.kt", "Type.kt", "Theme.kt"]:
              continue

            source["warn_files"].append({
              "file_name": file_name,
              "package_name": package_name,
              "percent_match": percent_match
            })


      return source

