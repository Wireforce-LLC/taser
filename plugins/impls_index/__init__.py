import json
import platform
import re
import subprocess

import packaging
from packaging import version

import requests

from core.cp import get_cp
from sdk.require_android_path import require_android_gradlew_path


def main():
  if platform.system() == "Windows":
    return "Windows not supported"

  path = require_android_gradlew_path()

  if not path:
    return "it is not possible to get imlements because you are outside the source directory"

  output = subprocess.check_output([
    '/bin/bash', path, 'app:dependencies', '--configuration', 'implementation'
  ], cwd=get_cp())

  all_implementations = re.findall(r'\+--- (.*?) \(n\)', str(output))
  impls = []

  for i in all_implementations:
    lib = i.split(':')[0]
    artifact = i.split(':')[1]
    v = i.split(':')[-1]
    up_to_date = None

    url = f'https://search.maven.org/solrsearch/select?q=g:"{lib}"+AND+a:"{artifact}"&rows=20&wt=json'

    libs = requests.get(url).json().get("response", {}).get("docs", [])

    try:
      version.parse(v)
    except packaging.version.InvalidVersion:
      v = None

    try:
      last_version = None

      try:
        last_version = libs[0].get('latestVersion', None)
      except:
        pass

      up_to_date = version.parse(v) >= version.parse(last_version)
    except packaging.version.InvalidVersion: pass
    except TypeError: pass


    if libs:
      impls.append(
        {
          'g': lib,
          'a': artifact,
          'v': v,
          'lv': libs[0].get('latestVersion', None),
          'utd': up_to_date
        },
      )

    else:
      impls.append(
        {
          'g': lib,
          'a': artifact,
          'v': v,
          'lv': None,
          'utd': None
        }
      )

  open(get_cp() + "/implementations_map.json", 'w+').write(json.dumps(impls))

  return impls
