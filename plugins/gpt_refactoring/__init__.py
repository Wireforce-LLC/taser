import json
import os.path
import re
import time

from prompt_toolkit.shortcuts import yes_no_dialog
from rich.panel import Panel

import plugins.source_map
from rich.progress import Progress
from rich.layout import Layout
from rich import print

from plugin_config import get_plugin_config
import openai


open_ai_key = get_plugin_config("openai")['key']
openai.api_key = open_ai_key

MODEL_REFACTOR_FILE_PATH = './models/refactor.file.json'

def show_compare(text1="N/A", text2="N/A"):
  layout = Layout()

  layout.split_row(
    Layout(name="upper", renderable=Panel(text1, highlight=True)),
    Layout(name="lower", renderable=Panel(text2, highlight=True))
  )

  print(layout)


def main():
  model = []

  vc_old_content = {}
  vc_new_content = {}


  files = plugins.source_map.main("read")

  if isinstance(files, str):
    return files

  if not open_ai_key:
    return "not set `open_ai_key`"

  if os.path.isfile(MODEL_REFACTOR_FILE_PATH):
    inject = json.loads(open(MODEL_REFACTOR_FILE_PATH, 'r').read())
    model = list(inject)

  with Progress() as progress:
    tasks = {}

    for file in files:
      basename = os.path.basename(file)

      stream = open(file, 'r').read()
      tokens = len(re.findall(r'\w+', stream))

      tasks[basename] = progress.add_task(f"[orange]{basename} (t: {tokens})", total=100)

    for file in files:
      basename = os.path.basename(file)

      stream = open(file, 'r').read()
      tokens = len(re.findall(r'\w+', stream))

      progress.update(tasks[basename], advance=20)

      chat = model + [
        {
          "role": "user",
          "content": stream
        }
      ]

      vc_old_content[basename] = stream

      # create a completion
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat
      )

      # print the completion
      result = completion.choices[0].get('message', {}).get('content', 'N/A')

      vc_new_content[basename] = result

      progress.update(tasks[basename], advance=60)

      if result:
        time.sleep(1.5)

        open(file, 'w+').write(result)

      progress.update(tasks[basename], advance=20)
      time.sleep(0.3)

    time.sleep(1)

    do_compare = yes_no_dialog(
      title='Want to compare the code?',
      text='The system saved the versions of the code before and after processing. Do you want to compare them in the visual editor?'
    ).run()

  if do_compare:
    i = 0

    while True:
      try:
        a_key = os.path.basename(files[i])

        show_compare(
          vc_old_content.get(a_key, "N/A"),
          vc_new_content.get(a_key, "N/A")
        )

        i = i + 1

        input("(NEXT?) />")

      except:
        break

