import os.path
import random
import string
import subprocess
from os import mkdir

import ppadb.device
from ppadb.client import Client as AdbClient

from libs import libs_config, get_lib_link
from shlex import quote as shlex_quote

adb_lib_path = get_lib_link('adb')


def is_port_in_use(port: int) -> bool:
  import socket
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    return s.connect_ex(('localhost', port)) == 0


if is_port_in_use(5037):
  client = AdbClient(host="127.0.0.1", port=5037)
else:
  client = None


def open_app(device: str | ppadb.device.Device, app_id: str):
  if not isinstance(device, ppadb.device.Device):
    device = client.device(device)

  return device.shell(f"monkey -p {app_id} -c android.intent.category.LAUNCHER 1")


def take_screenshot(device: str | ppadb.device.Device):
  if not isinstance(device, ppadb.device.Device):
    device = client.device(device)

  result = device.screencap()
  letters = string.ascii_lowercase
  name = ''.join(random.choice(letters) for i in range(10))
  png_path = f"./mount/screencap/{name}.png"

  if not os.path.isdir("./mount/screencap/"):
    mkdir("./mount/screencap/")

  with open(png_path, "wb") as fp:
    fp.write(result)

  return os.path.abspath(png_path)
