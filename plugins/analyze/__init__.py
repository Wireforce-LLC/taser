import json
import os.path
import re

import openai

from cp import get_cp

openai.api_key = "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"

MODEL_ANALYZE_IMPL_PATH = './models/analyze.impl.json'
MODEL_ANALYZE_SOURCE_PATH = './models/analyze.source.json'
MODEL_ANALYZE_SOURCE_SECURITY_PATH = './models/analyze.source.security.json'


def main(model='impl', meta=''):
  if model == "impl":
    model = []

    if not os.path.isfile(get_cp() + "/implementations_map.json"):
      return "Do not found impl map"

    impls = json.loads(open(get_cp() + "/implementations_map.json", 'r').read())

    if os.path.isfile(MODEL_ANALYZE_IMPL_PATH):
      inject = json.loads(open(MODEL_ANALYZE_IMPL_PATH, 'r').read())
      model = list(inject)

    chat = model + [
      {
        "role": "user",
        "content": ", ".join(impls)
      }
    ]

    # create a completion
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=chat
    )

    # print the completion
    print(completion.choices[0].get('message', {}).get('content', 'N/A'))

  if model == "source":
    model = []

    if not os.path.isfile(get_cp() + "/source_map.json"):
      return "Do not found source map"

    source_map = json.loads(open(get_cp() + "/source_map.json", 'r').read())

    fjava = source_map.get('fjava', [])
    fkt = source_map.get('fkt', [])

    files = fjava + fkt
    sources_chat_messages = []

    for file in files:
      if os.path.isfile(file):
        file_name = os.path.basename(file)
        stream = open(file, 'r').read()
        tokens = len(re.findall(r'\w+', stream))

        print(f"[{tokens < 300}] [{tokens}]: {file}")

        if tokens > 300:
          continue

        sources_chat_messages.append({
          "role": "user",
          "content": f"this is the content of the file {file_name}: {stream}"
        })

    used_model_file = MODEL_ANALYZE_SOURCE_PATH

    if meta == "safe":
      used_model_file = MODEL_ANALYZE_SOURCE_SECURITY_PATH

    if os.path.isfile(used_model_file):
      inject = json.loads(open(used_model_file, 'r').read())
      model = list(inject)

    chat = model + sources_chat_messages

    # create a completion
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=chat
    )

    # print the completion
    print(completion.choices[0].get('message', {}).get('content', 'N/A'))


def hints():
  return {
    'impl': None,
    'source': {
      'safe': None
    },
  }
