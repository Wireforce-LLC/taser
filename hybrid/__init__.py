import hashlib
import json
import os
import pathlib
import shutil
import time
import tempfile
import zipfile
import qrcode
import yaml
from git import Repo

from qrcode import QRCode
from rich.progress import Progress
from telethon import TelegramClient, events
from telethon.tl.custom import QRLogin
from rich.console import Console
from telethon.tl.functions.messages import SendReactionRequest

import hybrid
import inspectors
from cp import set_cp
from inspectors.hybrid_autotest import es
from sdk.is_android_dir import is_android_dir
from sdk.validation import validate_path_list_is_a_android_studio_project, find_files

console = Console()

hybrid_configs = {}

with open("./hybrid.yml", 'r') as document:
  hybrid.hybrid_configs = yaml.safe_load(document)


# Remember to use your own values from my.telegram.org!
api_id = hybrid_configs.get('telegram_api_id')
api_hash = hybrid_configs.get('telegram_api_hash')
client = TelegramClient('./mount/taser_account_2', api_id, api_hash)

TASER_CLOUD_URL = hybrid_configs.get('taser_cloud_url')


def sizeof_fmt(num, suffix="B"):
  for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"

@client.on(events.NewMessage(pattern='(?i)getPing'))
async def handler(event):
  await event.respond('Obtain pong')


@client.on(events.NewMessage(pattern='(?i)getMem'))
async def handler(event):
  # Path
  path = "./mount"

  # Get the disk usage statistics
  # about the given path
  stat = shutil.disk_usage(path)

  await event.respond('Obtain mem: ' + str(sizeof_fmt(stat.free)))


@client.on(events.NewMessage(pattern='(?i)getScore'))
async def handler(event):

  if event.reply_to:
    reply = await event.message.get_reply_message()

    if not reply.media:
      return

    if not reply.media.document:
      return

    if reply.media.document.attributes:
      filename = reply.media.document.attributes[0].file_name

    rep = es.search(index="report", query={
       'match': {
          'meta.filename': str(filename)
        }
    })

    total_found = rep.body.get('hits').get('total').get('value')

    if total_found:
      await event.respond('Total: ' + str(total_found))

      for hit in rep.body.get('hits').get('hits'):
        await event.respond("\n".join(
          [
            "Score: " + str(hit.get('_source').get('score').get('score')),
            "Namespace: " + str(hit.get('_source').get('namespace_app'))
          ]
        ))

    else:
      await event.respond('I dont know ' + str(filename))


@client.on(events.NewMessage)
async def my_event_handler(event):
  sender_id = event.message.peer_id
  user_id = None
  filename = None
  zip_created_at = None

  if event.fwd_from:
    sender_id = event.fwd_from.from_id

  if sender_id:
    user_id = sender_id.user_id

  if not event.media:
    return

  if not event.media.document:
    return

  if event.media.document.attributes:
    filename = event.media.document.attributes[0].file_name

  if event.media.document.date:
    zip_created_at = event.media.document.date

  if not event.media.document.mime_type == 'application/zip':
    return

  final_source_path = f"./mount/sources/{event.media.document.id}"

  if os.path.isdir(final_source_path):
    for dir in os.scandir(final_source_path):
      gradle_root_dir_name_build_optimize = final_source_path + "/" + dir.name + "/app/build"

      if os.path.isdir(gradle_root_dir_name_build_optimize):
        # Optimize size
        console.log("🗄 Privileged storage optimization...")
        shutil.rmtree(gradle_root_dir_name_build_optimize)
        console.log("🗄 Storage optimized")

    console.log("📍 This source has already been analyzed ")
    return

  console.log("👻 Source code accepted for analysis")

  output = await client.download_media(
    event.media,
    os.path.normpath(tempfile.gettempdir() + "/" + str(time.time()) + '.zip'),
    progress_callback=lambda x, y: console.log(
      f"📁 Download... {x}/{y}"
    ) if x % 5024 == 0 else None
  )

  file = zipfile.ZipFile(output, "r")
  files_join = ";".join(x for x in file.namelist() if not x.endswith('/'))

  md5 = hashlib.md5(files_join.encode()).hexdigest()

  if os.path.isfile("./mount/projects.md5"):
    with open("./mount/projects.md5", 'r') as r:
      for project in r.readlines():
        if project.strip() == md5.strip():
          console.log("📍 This source has already been analyzed [by MD5]")
          return

  with open("./mount/projects.md5", "a+") as a:
    a.write(f"{md5}\n")

  file = zipfile.ZipFile(output, "r")
  files = [x for x in file.namelist() if x.endswith('/')]

  is_android_source = validate_path_list_is_a_android_studio_project(files)

  console.log(f"🤖 Passed: {is_android_source}")

  android_source_inside_this_dir = None

  if not is_android_source:
    for file in file.namelist():
      if "app/src/main/" in file:
        android_source_inside_this_dir = file.split('app/src/main/')[0]
        break


  if not is_android_source and not android_source_inside_this_dir:
    if os.path.isfile(output):
      os.remove(output)
      return

  final_zip_path = f"./mount/sources/{os.path.basename(output)}"

  os.rename(output, final_zip_path)

  if not os.path.isfile(final_zip_path):
    return

  with zipfile.ZipFile(final_zip_path, 'r') as zip_ref:
    zip_ref.extractall(final_source_path)

  os.remove(final_zip_path)

  if android_source_inside_this_dir:
    source_dir = os.path.normpath(final_source_path + '/' + android_source_inside_this_dir)

    console.log(f"Transferring source code from '{source_dir}' to '{source_dir}'")

  gradles = find_files("gradle.properties", final_source_path)

  if len(gradles) == 1:
    gradle_root_dir_name = os.path.abspath(os.path.dirname(gradles[0]))

    if is_android_dir(gradle_root_dir_name):
      gradle_root_dir_name_build_optimize = gradle_root_dir_name + "/app/build/"
      
      # Optimize size
      if os.path.isdir(gradle_root_dir_name_build_optimize):
        console.log("🗄 Optimizing storage...")
        shutil.rmtree(gradle_root_dir_name_build_optimize)
        console.log("🗄 Storage optimized")

      repo = Repo.init(gradle_root_dir_name)
      repo.git.add(all=True)
      repo.index.commit("Created source code")

      set_cp(gradle_root_dir_name)

      inspectors.start_inspector('hybrid_autotest', gradle_root_dir_name, {
        "sender_id": user_id,
        "filename": filename,
        "zip_created_at": zip_created_at
      })

  else:
    for f in gradles:
      os.remove(os.path.abspath(f))

  # client.loop.run_until_complete(client.download_file(event.media.document))


def thread_main():
  if client.disconnected:
    client.loop.run_until_complete(client.connect())

    if not client.loop.run_until_complete(client.is_user_authorized()):
      client.loop.run_until_complete(client.connect())

      r = False

      while not r:
        qr: QRLogin = client.loop.run_until_complete(client.qr_login())

        qr_code = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=4,
        )

        qr_code.add_data(qr.url)
        qr_code.make(fit=True)
        qr_code.print_ascii()

        try:
          r = client.loop.run_until_complete(qr.wait(10))
        except:
          client.loop.run_until_complete(qr.recreate())

      console.log("Connected!")

  # client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))


def main():
  print("")
  thread_main()