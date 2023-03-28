import copy
import os
from os import path
from random import randint

from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.layout import ConditionalContainer, VSplit, Window, HSplit, Layout, FormattedTextControl, Float, \
  CompletionsMenu, WindowAlign, ScrollablePane, Dimension, Container, VerticalAlign, HorizontalAlign
from prompt_toolkit.lexers import DynamicLexer, PygmentsLexer
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea, MenuContainer, MenuItem, Frame, Button, Box

from cp import get_cp, format_cp
from plugins import source_map

PROMPT_TOOLKIT_ARGS = ""

kb = KeyBindings()
kb.add("tab")(focus_next)


@kb.add('c-q')
def exit_(event: KeyPressEvent) -> None:
  """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
  event.app.exit()


# layout = VSplit([
#     Window(BufferControl(), style='class:left'),
#     HSplit([
#         Window(BufferControl(), style='class:top'),
#         Window(BufferControl(), style='class:bottom'),
#     ], style='class:right')
# ])


# style = Style([
#      ('left', 'bg:ansired'),
#      ('top', 'fg:#00aaaa'),
#      ('bottom', 'underline bold'),
#  ])

# buff = Buffer(completer=animal_completer, complete_while_typing=True)
buff = Buffer()

files = source_map.main("read")

if not isinstance(files, list):
  files = []

search_toolbar = SearchToolbar()
text_field = TextArea(
  lexer=DynamicLexer(
    lambda: PygmentsLexer.from_filename(
      ".txt", sync_from_start=False
    )
  ),
  style="bg:#121212",
  focus_on_click=True,
  wrap_lines=True,
  scrollbar=True,
  line_numbers=True,
  search_field=search_toolbar,
)

body = HSplit(
  [
    text_field,
    search_toolbar,
    ConditionalContainer(
      content=VSplit(
        [
          Window(
            FormattedTextControl(
              "dir: " + get_cp()
            ), style="class:status"
          ),
          Window(
            FormattedTextControl(
              format_cp()
            ),
            style="class:status.right",
            width=9,
            align=WindowAlign.RIGHT,
          ),
        ],
        height=1,
      ),
      filter=Condition(lambda: "d"),
    ),
  ]
)

files_buttons = []

def open_file_lambda(file):
  def _():
    with open(file, 'r') as f:
      file_name, file_extension = os.path.splitext(file)

      text_field.lexer = DynamicLexer(
        lambda: PygmentsLexer.from_filename(file_extension, sync_from_start=False)
      )

      text_field.buffer._set_text(f.read())
  

    return None

  return _

for file in files:
  filename = copy.deepcopy(file)

  files_buttons.append(
    Button(
      path.split(file)[-1],
      left_symbol="",
      right_symbol="",
      handler=open_file_lambda(filename)
    )
  )

root_container = MenuContainer(
  body=VSplit(
    [
      ScrollablePane(
        HSplit(
          files_buttons,
          align=VerticalAlign.TOP
        ),
        width=30,
        keep_cursor_visible=True
      ),
      body
    ],

    style="bg:#131313"
  ),
  menu_items=[
    MenuItem(
      "File",
      children=[
        # MenuItem("New...", handler=do_new_file),
        # MenuItem("Open...", handler=do_open_file),
        # MenuItem("Save"),
        # MenuItem("Save as..."),
        # MenuItem("-", disabled=True),
        # MenuItem("Exit", handler=do_exit),
      ],
    ),
  ],
  floats=[
    Float(
      xcursor=True,
      ycursor=True,
      content=CompletionsMenu(max_height=16, scroll_offset=1),
    ),
  ],
  key_bindings=kb,
)

layout = Layout(
  root_container,
  focused_element=text_field
)

style = Style.from_dict(
  {
    "editor": "#fff",
    "status": "reverse",
    "shadow": "bg:#440044",
  }
)

app = Application(
  full_screen=True,
  key_bindings=kb,
  mouse_support=True,
  enable_page_navigation_bindings=True,
  style=style,
  color_depth=ColorDepth.DEPTH_24_BIT,
  layout=layout
)

def telnet():
  return "Some software is included in the Taser suite and only works on a local computer. " \
         "This programme is included in the Taser suite"

def main():
  app.run()
