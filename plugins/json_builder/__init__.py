import json
from prompt_toolkit import PromptSession

PROMPT_TOOLKIT_ARGS = ""

def telnet():
  return "Some software is included in the Taser suite and only works on a local computer. " \
         "This programme is included in the Taser suite"


def main():
  print(
    "You can now enter data on multiple lines.\n"
    "Each new line will take you to a new line.\n"
    "To finish editing, type exit_please"
  )

  temp_session = PromptSession()

  text = ""

  while True:
    line_number = 1

    line_read = temp_session.prompt(f"{line_number}  | ")

    if line_read == "exit_please":
      return json.dumps(json.loads(text))

    text = f"{text}\n{line_read}"

