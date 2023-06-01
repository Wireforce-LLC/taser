import sys

import pretty_traceback
import pyfiglet
import yaml
from frosch import hook, print_exception
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style
from pygments.lexers.python import Python3Lexer
from rich import pretty
from rich.console import Console

import adapter.telnet
from core import executor
import inspectors
from core.cp import format_cp

hook()

pretty.install()

pretty_traceback.install()
our_history = FileHistory("./mount/.history")
console = Console()

# The history needs to be passed to the `PromptSession`. It can't be passed
# to the `prompt` call because only one history can be used during a
# session.
session = PromptSession(history=our_history)

style = Style.from_dict({
  # User input (default text).
  '': 'white bold',

  # Prompt.
  'name': 'ansicyan bold',
  'pound': '#00aa00 default',
  'user_prompt': 'bold',
  'path': 'yellow underline',
})

last_result = None
local_plug_namespace = {}

if __name__ == '__main__':
  ascii_banner = pyfiglet.figlet_format("Taser://")

  print(ascii_banner)
  console.print("Taser Prism is an open source program designed to\nanalyze the source code of android applications")

  print("")

  with open("data/lib_detect.yml", 'r') as document:
    console.print(f"The system is able to identify [orange]{len(yaml.safe_load(document).get('libs').keys())}[/] technologies that were used in the source code and assess their importance")

  with open("./mount/unicorn.txt", 'r') as document:
    console.print(f"Unicorn allows you to check libraries for the latest versions. The repository now has [orange bold]{len(document.readlines())}[/] libraries")

  console.print("Taser also supports the [red bold]Revisoro[/] utilities and the newer [red bold]Ro2[/] version to analyze code inheritance out of the box ")

  print("")

  inspectors.init()


  if 'telnet' in sys.argv:
    console.print("🌍 Expansion to the world!!! You use telnet mode. ")

    adapter.telnet.main()

  while True:
    try:
      message = [
        ('class:name', "taser"),
        ('', ':'),
        ('class:path', f"{format_cp()}"),
        ('class:pound', '/> '),
        ('class:user_prompt', ''),
      ]

      text = session.prompt(
        message,

        lexer=PygmentsLexer(Python3Lexer),
        completer=NestedCompleter.from_nested_dict(executor.completer_dict),
        style=style,
        # bottom_toolbar=get_toolbar,
        # mouse_support=True,
        clipboard=PyperclipClipboard(),
        complete_style=CompleteStyle.COLUMN,
        enable_history_search=True,
        refresh_interval=0.5,
        # lexer=get_lexer_by_name('Python'),
        auto_suggest=AutoSuggestFromHistory(),
        color_depth=ColorDepth.TRUE_COLOR
      )

      try:
        if text in sys.argv:
          exclude = executor.input_execute(text)

          if not isinstance(exclude, list):
            console.print(
              exclude,
              highlight=True,
              no_wrap=False,
              markup=True
            )

          else:
            for line in exclude:
              console.print(
                line,
                highlight=True,
                no_wrap=False,
                markup=True
              )

      except Exception as error:
        print_exception(error)

    except KeyboardInterrupt:
      exit(0)
