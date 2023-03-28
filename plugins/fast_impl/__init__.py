import re

from sdk.require_android_path import require_android_build_gradle_app_path

PROMPT_TOOLKIT_ARGS = ""

def main():
  gradle_path = require_android_build_gradle_app_path()

  gradle = open(gradle_path, "r").read()

  dependencies_array = []

  for line in gradle.split('\n'):
    groups = re.search(
      r"implementation\s'(?P<g>[\w\.]+):(?P<pgk>[\w\-]+):(?P<version>[\d\.]+)'",
      line
    )
    if groups:
      dependencies_array.append({
        'g': groups.group('g'),
        'pgk': groups.group('pgk'),
        'version': groups.group('version')
      })

  return dependencies_array