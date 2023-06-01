import os.path

import yaml
from sys import platform

libs_config = {}

with open("data/libs.yml", 'r') as document:
  libs_config = yaml.safe_load(document)


def get_libs_links():
  if platform == "linux" or platform == "linux2":
    return libs_config.get("libs", {}).get("linux", {})

  elif platform == "darwin":
    return libs_config.get("libs", {}).get("macosx", {})

  elif platform == "win32":
    return libs_config.get("libs", {}).get("win32", {})


def get_lib_link(lib: str):
  return os.path.abspath(get_libs_links().get(lib, None))