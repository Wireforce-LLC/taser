import importlib
import pkgutil

from rich.console import Console

import adb
import plugins
from cp import get_cp

is_telnet = False
console = Console()

def iter_namespace(ns_pkg):
  return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


completer_dict = {}

discovered_plugins = {
  name: importlib.import_module(name)
  for finder, name, ispkg
  in iter_namespace(plugins)
}

for plug in discovered_plugins:
  def proxy(x: str):
    def _(*varargs):
      out = []

      if hasattr(discovered_plugins[x], "PROMPT_WELCOME"):
        if is_telnet:
          print(discovered_plugins.get(x).PROMPT_WELCOME)

        else:
          console.print(discovered_plugins.get(x).PROMPT_WELCOME)

      if hasattr(discovered_plugins[x], "telnet"):
        vars()['_f'] = x
        return discovered_plugins.get(x).telnet(*varargs)


      if hasattr(discovered_plugins[x], "main") and \
          not hasattr(discovered_plugins[x], "telnet"):

        vars()['_f'] = x
        return discovered_plugins.get(x).main(*varargs)

      return None

    return _


  key = plug.replace('plugins.', 'plug_') + "()"
  completer_dict[key] = None

  if hasattr(discovered_plugins[plug], "hints"):
    completer_dict[key] = discovered_plugins[plug].hints()

  vars()['plug_%s' % plug.replace('plugins.', '')] = proxy(plug)
  vars()['_%s' % plug.replace('plugins.', '')] = proxy(plug)
  # main.local_plug_namespace[plug.replace('plugins.', '')] = proxy(plug)


def input_execute(text: str):
  vars()['_adb_devices_'] = adb.client.devices()
  vars()['_java_'] = discovered_plugins['plugins.teleport_src_main_java'].main()
  vars()['PWD'] = get_cp()
  vars()['eval'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
  vars()['exec'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
  vars()['os'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
  vars()['path'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
  vars()['import'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
  globals()['os'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")

  last_result = exec(
    f"globals()['__'] = {text}"
  )

  globals()['_'] = last_result
  globals()['_r'] = last_result
  globals()['_q'] = text

  return globals()['__']
