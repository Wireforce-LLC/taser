import glob

from sdk.require_android_path import require_android_xml_layout_path


def get_list_layouts_path(path: str = require_android_xml_layout_path()):
  return list(glob.glob(f"{path}/*.xml", recursive=True))
