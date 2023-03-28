import os.path
import random
import subprocess
from time import time

from cp import get_cp
from libs import get_lib_link

detekt_lib_path = get_lib_link('detekt')


def main(auto_correct=False, debug=True):
  if not detekt_lib_path:
    return "detekt not selected in libs.yml"

  abs_path_to_report = os.path.normpath(f"{os.path.abspath(get_cp())}/report_{time()}.xml")

  subprocess.run(
    f"{detekt_lib_path} --all-rules {'-ac' if auto_correct else ''} {'--debug' if debug else ''} -r xml:{abs_path_to_report}",
    shell=True,
    cwd=os.path.abspath(get_cp())
  )

  return abs_path_to_report

