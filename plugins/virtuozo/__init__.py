import json
from rich.console import Console
from rich import inspect

import plugins.source_map
import sdk.manifest

console = Console()

def main():
  activities = sdk.manifest.read_activities()
  source_map = plugins.source_map.main('index')

  inspect({
    "activities": activities,
    "sources": source_map
  })


