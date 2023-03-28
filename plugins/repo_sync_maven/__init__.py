#!/usr/local/bin/python3

import requests
import xmltodict
from rich.console import Console

console = Console()

# TODO:
#   multi-thread

def main():
  r = requests.get('https://repo1.maven.org/maven2/archetype-catalog.xml')
  data = xmltodict.parse(r.text)

  catalog = []
  prev_artifact_id = ""

  for archetype in data['archetype-catalog']['archetypes']['archetype']:
    if prev_artifact_id and prev_artifact_id != archetype['artifactId']:
      console.log(f"[MavenSync] {archetype['groupId']}:{archetype['artifactId']}:{archetype['version']}")

      catalog.append({
        'g': archetype['groupId'],
        'pkg': archetype['artifactId'],
        'version': archetype['version']
      })

    prev_artifact_id = archetype['artifactId']

  return catalog
