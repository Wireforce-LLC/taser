import os.path

import plugins.source_map

def main():
  files = plugins.source_map.main("read")

  if isinstance(files, str):
    return files

  pkgs = []

  for file in files:
    if os.path.isfile(file):
      with open(file, 'r') as file:
        lines = file.readlines()
        file.close()

      for line in lines:
        if line.startswith("import"):
          pkg = line.strip().replace(";", "").replace("import ", "")

          if not " " in pkg and not "*" in pkg:
            pkgs.append(pkg)

  return sorted(list(set(pkgs)))