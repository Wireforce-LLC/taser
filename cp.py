import os
from os import path


def format_cp():
  return path.split(get_cp())[-1]


def get_cp():
    cpath = open(".cpath", 'r+').read()

    return path.normpath(path.realpath(cpath))


def set_cp(cp):
    if not path.isdir(cp):
        return False

    if not os.listdir(cp):
        return False

    if " " in cp:
      print("WARNING!! Your folder contains spaces. Some plugins may not work correctly ")

    open(".cpath", 'w+').write(path.normpath(cp))

    return path.normpath(path.realpath(cp))

