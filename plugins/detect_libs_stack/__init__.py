import yaml

import plugins.detect_all_imports

lib_detect = {}

with open("data/lib_detect.yml", 'r') as document:
  lib_detect = yaml.safe_load(document)

def detect_stack(imports, stack_required):
  return all(elem in imports for elem in stack_required)

def main():
  imports = plugins.detect_all_imports.main()
  stack = []
  libs = lib_detect.get("libs", [])

  for lib in libs:
    check_imports = libs[lib].get("imports", None)

    if check_imports:
      if detect_stack(imports, check_imports):
        stack.append({
          "id": lib,
          "lib": libs[lib]
        })

  return stack