import os.path
import re

from sdk.require_android_path import require_android_build_gradle_app_path


def get_namespace():
  gradle_path = require_android_build_gradle_app_path()

  with open(os.path.abspath(gradle_path), 'r') as file:
      gdoc = file.read()
      file.close()

  result1 = re.search('applicationId \'(.*)\'', gdoc)
  result2 = re.search('applicationId "(.*)"', gdoc)

  if result1:
      return result1.group(1)

  if result2:
      return result2.group(1)

  return None

