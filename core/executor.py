import importlib
import os
import pkgutil

from rich.console import Console
from core.cp import get_cp

is_telnet = False
console = Console()
env = dict(locals(), **globals())

def get_directories_in_directory(directory):
    directories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            directories.append(item_path)
    return directories


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

completer_dict = {}

def initPlugins(includesPlugins = []):
    discovered_plugins = {}
    for i in get_directories_in_directory("plugins/"):
        if includesPlugins != [] and i.split('/')[1] not in includesPlugins:
            continue

        discovered_plugins[i.replace("/", '.')] = importlib.import_module(i.replace("/", '.'))

    for plug in discovered_plugins:
        def proxy(x: str):
            def _(*varargs):
                out = []

                if hasattr(discovered_plugins[x], "PROMPT_WELCOME"):
                    if is_telnet:
                        print(discovered_plugins.get(x).PROMPT_WELCOME)

                    else:
                        console.print(discovered_plugins.get(x).PROMPT_WELCOME)

                if is_telnet and hasattr(discovered_plugins[x], "telnet"):
                    vars()['_f'] = x
                    return discovered_plugins.get(x).telnet(*varargs)

                if hasattr(discovered_plugins[x], "main") and \
                      not is_telnet:
                    vars()['_f'] = x
                    return discovered_plugins.get(x).main(*varargs)

                return None

            return _

        key = plug.replace('plugins.', 'plug_') + "()"
        completer_dict[key] = None

        if hasattr(discovered_plugins[plug], "hints"):
            completer_dict[key] = discovered_plugins[plug].hints()

        env['plug_%s' % plug.replace('plugins.', '')] = proxy(plug)
        env['_%s' % plug.replace('plugins.', '')] = proxy(plug)

def input_execute(text: str):
    env['PWD'] = get_cp()

    env['eval'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
    env['exec'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
    env['os'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
    env['path'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")
    env['import'] = lambda x: print("Hey! What are you up to? These operations are blocked for security reasons")

    inline = text.strip()

    if len(inline.split(" ")) == 1:
        if f"_{inline}" in env.keys():
            text = f"_{inline}()"

    if len(inline.split(" ")) == 2:
        inline_complex = inline.split(" ")

        if f"_{inline_complex[0]}" in env.keys():
            text = f"_{inline_complex[0]}({inline_complex[1]})"

    last_result = exec(
        f"__ = {text}",
        env,
        env
    )

    env['_'] = last_result
    env['_r'] = last_result
    env['_q'] = text

    return env['__']
