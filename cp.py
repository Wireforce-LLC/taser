import os
from os import path


def format_cp():
  return path.split(get_cp())[-1]


def get_cp():
  with open(".cpath", 'r+') as file:
    cpath = file.read()
    file.close()

  return path.normpath(path.realpath(cpath))


def set_cp(cp):
  if not path.isdir(cp):
    return False

  if not os.listdir(cp):
    return False

  if " " in cp:
    print("WARNING!! Your folder contains spaces. Some plugins may not work correctly ")

  path_to = path.abspath(path.normpath(path.realpath(cp)))

  with open(".cpath", 'w+') as file:
    file.write(path_to)
    file.close()

  return path_to
