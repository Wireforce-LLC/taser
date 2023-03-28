from os import path

from cp import get_cp
from sdk.is_android_dir import is_android_dir
from sdk.validation import find_files


def require_android_path():
    if is_android_dir(get_cp()):
        return get_cp()
    else:
        return False

def require_android_manifest_path():
    android_path = require_android_path()
    manifest_path = str(android_path) + '/app/src/main/AndroidManifest.xml'

    if android_path:
        if path.isfile(manifest_path):
            return manifest_path

    return False


def require_android_strings_xml_path():
    android_path = require_android_path()
    xml_path = str(android_path) + '/app/src/main/res/values/strings.xml'

    if xml_path:
        if path.isfile(xml_path):
            return xml_path

    return False


def require_android_themes_xml_path():
  android_path = require_android_path()
  xml_path = str(android_path) + '/app/src/main/res/values/themes.xml'

  if xml_path:
    if path.isfile(xml_path):
      return xml_path

  return False


def require_android_package_by_root_path():
  android_path = require_android_path()

  if android_path:
    gradle_props_root = find_files("gradle.properties", android_path)

    if gradle_props_root:
      return gradle_props_root[0]

  return None

def require_android_nav_graphs_path():
  android_path = require_android_path()
  xml_path = str(android_path) + '/app/src/main/res/navigation'

  if xml_path:
    if path.isdir(xml_path):
      return xml_path

  return False


def require_android_xml_layout_path():
  android_path = require_android_path()
  xml_path = str(android_path) + '/app/src/main/res/layout'

  if xml_path:
    if path.isdir(xml_path):
      return xml_path

  return False

def require_android_colors_xml_path():
  android_path = require_android_path()
  xml_path = str(android_path) + '/app/src/main/res/values/colors.xml'

  if xml_path:
    if path.isfile(xml_path):
      return xml_path

  return False


def require_android_gradlew_path():
    android_path = require_android_path()
    gradlew_path = str(android_path) + '/gradlew'

    if android_path:
        if path.isfile(gradlew_path):
            return gradlew_path

    return False


def require_android_build_gradle_app_path():
  android_path = require_android_path()
  gradle_path = str(android_path) + '/app/build.gradle'

  if android_path:
    if path.isfile(gradle_path):
      return gradle_path

  return False