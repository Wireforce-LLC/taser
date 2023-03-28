from threading import Thread

import plugins.gradle
import adb
from sdk.build_gradle_parser import get_namespace
from rich.console import Console

def test(path, meta):
  print("Hello")

  devices = adb.client.devices()

  if not devices:
    return "Not devices attached"

  plugins.gradle.main("installDebug")

  adb.open_app(devices[0], get_namespace())

  Thread(target=lambda: main(path)).run()


def main(path):
  from uiautomator import device as d

  d.screen.on()
  d.wakeup()

  d.wait.idle()
  # wait until window update event occurs
  d.wait.update()

  d.dump("hierarchy.xml")
  # or get the dumped content(unicode) from return.
  xml = d.dump()

  Console().print(xml)
  Console().print(d.info)

  # d.press.home()

  # adb.client.

  exit(0)