from os import path

PROMPT_TOOLKIT_ARGS = ""

def main(realpath):
  path_to = path.abspath(path.normpath(path.realpath(realpath)))

  with open(".cpath", 'w+') as file:
    file.write(path_to)
    file.close()
