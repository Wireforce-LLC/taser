import os

from cp import get_cp


def main(dir: str = get_cp()):
  prefix = '/app/src/main/java'

  dirs = [x[0] for x in os.walk(dir)]
  nested = []

  for d in dirs:
    if prefix in d:
      nested.append(d)

  try:
    return nested[0]
  except:
    return None