import os
from os import path


def is_android_dir(dir: str):
  if not path.isdir(dir):
    return False

  if 'build.gradle' in os.listdir(dir):
      if 'AndroidManifest.xml' in os.listdir(dir + "/app/src/main"):
          return True

  return False