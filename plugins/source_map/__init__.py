import glob
import json
import os

from core.cp import get_cp
from sdk.require_android_path import is_android_dir


def scan(dir_path: str, ext: str):
  res = []

  for file in os.listdir(dir_path):
    if file.endswith(ext):
      res.append(file)

  return res


def main(operation='index'):
  path = is_android_dir(get_cp())

  if not path:
    return "It is not possible to map source code files because you are outside the source directory"

  source_map_file = get_cp() + '/source_map.json'

  if operation == 'read':
    if not os.path.isfile(source_map_file):
      return "Source map not found. Try `source_map index`"

    with open(source_map_file, 'r') as file:
      source_map_dict = json.loads(file.read())
      file.close()

    files = []

    for fkt in source_map_dict.get('fkt', []):
      files.append(fkt)

    for fjava in source_map_dict.get('fjava', []):
      files.append(fjava)

    return files


  if operation == 'index':
    prefix = '/app/src/main/java'

    files_java = glob.glob(get_cp() + f"{prefix}/**/*.java", recursive=True)
    files_kotlin = glob.glob(get_cp() + f"{prefix}/**/*.kt", recursive=True)

    obj = {
      "fjava": files_java,
      "fkt": files_kotlin
    }

    with open(source_map_file, 'w+') as file:
        file.write(json.dumps(obj))
        file.close()

    return obj
