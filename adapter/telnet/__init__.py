import contextlib
import io
import json
import logging
import os
import shutil
import socket
import traceback
from asyncio import run, Future
from contextlib import closing
from datetime import datetime, time
from time import sleep
from pythonping import ping

import prompt_toolkit
import psutil
import pyfiglet
from frosch import hook, print_exception
from prompt_toolkit import print_formatted_text as print, ANSI

import yaml

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.contrib.telnet.server import TelnetServer
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.shortcuts import PromptSession, clear, CompleteStyle
from prompt_toolkit.styles import Style
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import Python3Lexer
from rich.console import Console

import pprint

from rich.traceback import Traceback

import executor
from adapter import telnet
from cp import format_cp

console = Console()
connections = []
server: socket = None

hook()

style = Style.from_dict({
  # User input (default text).
  '': 'white bold',

  # Prompt.
  'name': 'ansicyan bold',
  'pound': '#00aa00 default',
  'user_prompt': 'bold',
  'path': 'yellow underline',
})

telnet_configs = {}

with open("./telnet.yml", 'r') as document:
  telnet.telnet_configs = yaml.safe_load(document)


def find_free_port():
  with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
    s.bind(('', 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s.getsockname()[1]

def human_size(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
  """ Returns a human readable string representation of bytes """
  return str(bytes) + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])

async def interact(connection: prompt_toolkit.contrib.telnet.server.TelnetConnection):
  console.log("We have guests. Someone is trying to connect. As soon as they enter their password, you'll get a message about it")

  write = connection.send

  is_auth = False
  login_attempts = 0
  passwords_variants = []
  auth_login = None
  ascii_banner = pyfiglet.figlet_format("Taser Telnet://")

  clear()
  write(ascii_banner)
  write("\n")
  write("Welcome to Taser Telnet\n")
  write("* With great power comes great responsibility\n")
  write(
    "* Don't try to go outside the runtime system, because we can easily repair the container and you'll get fucked up\n")
  write("* Have fun! Make the most of your opportunities\n")
  write("\n")


  write("\n")
  write("We welcome you to a remote machine with great configurations.\n"
        f"You have {human_size(psutil.virtual_memory().total)} of RAM, {os.cpu_count()} processor core, and {human_size(shutil.disk_usage('/').free)} of free disk space\n")

  write("Is that enough fun for today? Just enter the command 'exit'\n")
  write("\n")
  write("\n")


  while not is_auth:
    if not is_auth:
      # Ask for input.
      temp_session = PromptSession()

      login_attempts += 1

      clog = await temp_session.prompt_async("Your login: ")
      cpass = await temp_session.prompt_async("Your password: ", is_password=True)

      if ':' in str(clog):
        auth_line = str(clog).split(':')

        clog = auth_line[0]
        cpass = auth_line[-1]

      if not clog or not cpass:
        connection.close()
        console.log("User changed his mind about logging in and logged out without entering his data ")

      passwords_variants.append(cpass)

      if f"{clog}:{cpass}" in telnet_configs.get('users', []):
        is_auth = True
        auth_login = clog

      if login_attempts > 3:
        connection.close()
        console.log(f"Someone was picking up passwords to user {clog}. "
                    f"Here are the variants the user tried to enter: " + ", ".join(passwords_variants))

  passwords_variants = []
  console.log(f"User {auth_login} has successfully logged on")

  message = [
    ('class:name', f"taser-telnet:{auth_login}"),
    ('', ':'),
    ('class:path', f"{format_cp()}"),
    ('class:pound', '//> '),
    ('class:user_prompt', ''),
  ]

  while is_auth:
    our_history = FileHistory(f"./mount/.telnet-history-{auth_login}")

    # Ask for input.
    session = PromptSession(history=our_history)

    try:
      result = await session.prompt_async(
        message=message,
        style=style,
        # bottom_toolbar=get_toolbar,
        # mouse_support=True,
        completer=NestedCompleter.from_nested_dict(executor.completer_dict),
        clipboard=PyperclipClipboard(),
        complete_style=CompleteStyle.COLUMN,
        enable_history_search=True,
        refresh_interval=0.5,
        lexer=PygmentsLexer(Python3Lexer),
        auto_suggest=AutoSuggestFromHistory(),
        color_depth=ColorDepth.TRUE_COLOR
      )

      if str(result) == "":
        continue

      if str(result) == 'exit':
        connection.close()

      if str(result) == 'ping':
        response_list = ping(connection.addr[0], size=40, count=10)

        connection.send_above_prompt(
          f"\n\n{response_list.rtt_avg_ms}ms"
        )

        continue

      output_stream = io.StringIO()

      with contextlib.redirect_stdout(output_stream):
        try:
          executor.is_telnet = True
          out = executor.input_execute(result)

          if isinstance(out, list):
            for line in out:
              if isinstance(line, dict):
                # Using my favorite style - monokai
                print(
                  ANSI(highlight(
                    json.dumps(line, indent=2),
                    lexer=get_lexer_by_name("json"),
                    formatter=Terminal256Formatter(style="monokai")
                  ))
                )

              else:
                if line != None:
                  print(
                    ANSI(highlight(
                      str(line),
                      lexer=get_lexer_by_name("bash"),
                      formatter=Terminal256Formatter(style="monokai")
                    ))
                  )

          else:
            if isinstance(out, dict):
              # Using my favorite style - monokai
              print(
                ANSI(highlight(
                  json.dumps(out, indent=2),
                  lexer=get_lexer_by_name("json"),
                  formatter=Terminal256Formatter(style="monokai")
                ))
              )

            else:
              if out != None:
                print(
                  ANSI(highlight(
                    str(out),
                    lexer=get_lexer_by_name("bash"),
                    formatter=Terminal256Formatter(style="monokai")
                  ))
                )

        except Exception as error:

          output_stacktrace = io.StringIO()

          with contextlib.redirect_stdout(output_stacktrace):
            print_exception(error)

          print(
            ANSI(output_stacktrace.getvalue())
          )

      output_stream = output_stream.getvalue()

      try:
        # Send output.
        connection.send_above_prompt(
          to_formatted_text(ANSI(output_stream), auto_convert=True)
        )

      except Exception as error:
        print_exception(error)
        # print(traceback.format_exc())

    except KeyboardInterrupt:
      print(
        "\n\n"
        "I'm sorry, but the administrators need to shut down the machine.\n"
        "The connection will be severed"
      )
      connection.close()
      exit(0)


async def main_server(port: int):
  server = TelnetServer(interact=interact, port=port)
  server.start()

  # Run forever.
  await Future()


def main():
  port = find_free_port()

  print(f"🖥  URL: telnet://{'localhost'}:{port} or")
  print(f"telnet {'localhost'} {port}")

  try:
    run(main_server(port))
  except SystemExit:
    exit(0)

  except KeyboardInterrupt:
    for connection in connections:
      try:
        connection.send_above_prompt(
          "\n\n"
          "I'm sorry, but the administrators need to shut down the machine.\n"
          "The connection will be severed"
        )
        connection.close()
      except:
        pass

    exit(0)
