import os
import time

from rich import inspect
from rich.console import Console
from multiprocessing.pool import ThreadPool

import plugins.repo_sync_maven
import plugins.repo_sync_google

console = Console()

PROMPT_TOOLKIT_ARGS = ""
PROMPT_WELCOME = "🦄 Unicorn library search utility"


def search(impl: str):
  with open('./mount/unicorn.txt', 'r') as file:
    lines = file.readlines()
    file.close()

  if os.path.isfile('./mount/unicorn.txt'):
    for i in lines:
      if i.startswith(impl.lower()):
        if ':' in i:
          parsed = i.strip().split(':')

          return {
            'g': parsed[0],
            'pkg': parsed[1],
            'version': parsed[2]
          }

  return None


def telnet(impl: str):
  start = time.time()

  result = search(impl)

  search_time = time.time() - start

  if result:
    return {
      "result": result,
      "meta": {
        "search_time_text": f"Search took {search_time}s"
      }
    }

def main():
  search_text = console.input("Which library do you want to find: [bold white]")

  start = time.time()

  result = search(search_text)

  search_time = time.time() - start

  if result:
    inspect(result)

  console.print(f"Search took {search_time}s")