import random

PROMPT_TOOLKIT_ARGS = "0, 1"


def main(min: int = 0, max: int = 1):
  return random.randint(min, max)
