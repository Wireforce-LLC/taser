import json

from prompt_toolkit import PromptSession

PROMPT_TOOLKIT_ARGS = ""

def main(data, mode="out"):
  if mode == "out":
    return json.dumps(data)

  elif mode == "in":
    return json.loads(data)
