import os.path
from datetime import datetime

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyPressEvent, KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.layout import FormattedTextControl, Window, VSplit, Layout, Container, UIContent
from rich.panel import Panel
from rich.progress import Progress
import plotext as plt
from rich.console import Console

console = Console()


def plt_ratio_tokens(prism_data):
  files_tokens = list(map(lambda x: os.path.basename(x), prism_data["tokenize"]["files_tokens"].keys()))
  files_tokens_size = prism_data["tokenize"]["files_tokens"].values()

  plt.simple_stacked_bar(files_tokens, files_tokens_size, width=150, title='File volume ratio')
  plt.show()


def plt_ratio_lines(prism_data):
  files_tokens = list(map(lambda x: os.path.basename(x), prism_data["tokenize"]["files_lines"].keys()))
  files_tokens_size = prism_data["tokenize"]["files_lines"].values()

  plt.simple_stacked_bar(files_tokens, files_tokens_size, width=150, title='File lines ratio')
  plt.show()


def plt_creation_files(prism_data):
  files_time_name = list(map(lambda x: datetime.fromtimestamp(x).strftime("%m/%d/%Y, [%H:%M]"), prism_data["source_creation_time"].values()))
  files_name = list(map(lambda x: os.path.basename(x), prism_data["source_creation_time"].keys()))
  files_time_int = list(map(lambda x: round(x), prism_data["source_creation_time"].values()))

  lines = []

  for i in files_name:
    index = files_name.index(i)

    lines.append(f"ct: {files_time_name[index]} ({files_time_int[index]}): {i}")

  console.print(
    Panel(
      "\n".join(lines),
      title="Search for temporal anomalies",
      highlight=True
    )
  )

def main(prism_data):
  plt_ratio_tokens(prism_data)
  plt_ratio_lines(prism_data)
  plt_creation_files(prism_data)

  console.print(Panel(
    f"Count tokens: [{'red' if prism_data['tokenize']['count_tokens'] <= 1000 else 'green'}]{prism_data['tokenize']['count_tokens']}[reset]\n"
    f"Count lines: [{'red' if prism_data['tokenize']['count_all_lines'] <= 500 else 'green'}]{prism_data['tokenize']['count_all_lines']}[reset]"
  ))
