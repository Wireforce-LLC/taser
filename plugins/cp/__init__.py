from core.cp import set_cp

PROMPT_TOOLKIT_ARGS = ""

def main(path):
  return f"Current path: {set_cp(path)}"
