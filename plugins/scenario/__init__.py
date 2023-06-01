import os

from core.cp import get_cp
from inspectors import start_inspector
from pick import pick

def main(name: str = None, path: str = get_cp()):
  if not name:
    list_of_dirs = [x.name for x in os.scandir('./inspectors')]

    list_of_dirs.remove(".DS_Store")
    list_of_dirs.remove("__init__.py")
    list_of_dirs.remove("__pycache__")

    inspector, index = pick(
      list_of_dirs,
      "Select screnario"
    )

    return start_inspector(inspector, path)

  return start_inspector(name, path)