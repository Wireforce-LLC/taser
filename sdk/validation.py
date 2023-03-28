import os

ANDROID_PATHS = [
  'app/',
  'app/src/',
  'app/src/main/',
  'app/src/main/java/',
  'app/src/main/res/',
  'app/src/main/res/drawable/',
  'app/src/main/res/layout/',
  'app/src/main/res/values/'
]


def find_files(filename, search_path):
  result = []

  for root, dir, files in os.walk(search_path):
    if filename in files:
      result.append(os.path.join(root, filename))

  return result


def validate_path_list_is_a_android_studio_project(paths: list):
  path_included = {}

  for android_path in ANDROID_PATHS:
    path_included[android_path] = False
    for path in paths:
      if android_path in path:
        path_included[android_path] = True
        continue

  return not False in path_included.values()