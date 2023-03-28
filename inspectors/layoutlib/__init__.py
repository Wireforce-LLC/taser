import logging

import numpy
import pandas as pd
import xarray
from rich import inspect

from sdk import layoutlib
from rich.console import Console

console = Console()

def test(path, meta):
  results = layoutlib.analyze_xml(path)

  for result in results:
    console.print(
      f'[bold red blink]{result.get("level")}[/]: {result.get("content")}'
    )
