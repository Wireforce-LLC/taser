import os
from multiprocessing.pool import ThreadPool
from threading import Thread

import plugins.repo_sync_maven
import plugins.repo_sync_google

PROMPT_TOOLKIT_ARGS = ""
PROMPT_WELCOME = "🦄 Welcome to unicorn dependency-sync manager"

UNICORN_TELNET_STATUS = "sleep"

def telnet(arg=""):
  if arg == "status":
    return "Status: " + UNICORN_TELNET_STATUS

  if arg == "sync":
    Thread(target=main).run()


  return "🦄 Unicorn on Telnet has a slightly reduced functionality. " \
       "You will not see the packet update process, because all of these processes will be done in the background. " \
       "You can check the execution status with the _unicorn(\"status\") command\n\n" \
       "To start synchronization, type _unicorn(\"sync\")"

def main():
  UNICORN_TELNET_STATUS = "start-sync"

  r_google = plugins.repo_sync_google.main()
  r_maven = plugins.repo_sync_maven.main()

  if os.path.isfile('./mount/unicorn.txt'):
    os.remove('./mount/unicorn.txt')

  UNICORN_TELNET_STATUS = "writing"

  for r in r_google + r_maven:
    with open('./mount/unicorn.txt', 'a+') as f:
      f.write(f'{r.get("g", "N/a")}:{r.get("pkg", "N/a")}:{r.get("version", "N/a")}' + "\n")

  UNICORN_TELNET_STATUS = "done"

  return f"🦄 [bold]Unicorn has successfully created a dependency map. Map size {len(r_google + r_maven)} libraries[/]"
