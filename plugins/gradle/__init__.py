import os
import platform
import subprocess

from core.cp import get_cp
from sdk.require_android_path import require_android_gradlew_path


def main(command=""):
  if platform.system() == "Windows":
    return "Windows not supported"

  path = require_android_gradlew_path()

  if not path:
    return "./gradlew not found"

  subprocess.run(
    f"/bin/bash {path} {command}",
    shell=True,
    cwd=os.path.abspath(get_cp())
  )
