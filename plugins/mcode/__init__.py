from rich.syntax import Syntax
from rich.traceback import Traceback

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, Static

from core.cp import get_cp


class CodeBrowser(App):
  """Textual code browser app."""

  CSS_PATH = "code_browser.css"
  BINDINGS = [
    ("f", "toggle_files", "Toggle Files"),
    ("q", "quit", "Quit"),
  ]

  show_tree = var(True)

  def watch_show_tree(self, show_tree: bool) -> None:
    """Called when show_tree is modified."""
    self.set_class(show_tree, "-show-tree")

  def compose(self) -> ComposeResult:
    """Compose our UI."""
    path = get_cp()

    yield Header()
    with Container():
      yield DirectoryTree(path, id="tree-view")
      with VerticalScroll(id="code-view"):
        yield Static(id="code", expand=True)
    yield Footer()

  def on_mount(self, event: events.Mount) -> None:
    self.query_one(DirectoryTree).focus()

  def on_directory_tree_file_selected(
      self, event: DirectoryTree.FileSelected
  ) -> None:
    """Called when the user click a file in the directory tree."""
    event.stop()
    code_view = self.query_one("#code", Static)
    try:
      syntax = Syntax.from_path(
        event.path,
        line_numbers=True,
        word_wrap=False,
        indent_guides=True,
        theme="github-dark",
      )
    except Exception:
      code_view.update(Traceback(theme="github-dark", width=None))
      self.sub_title = "ERROR"
    else:
      code_view.update(syntax)
      self.query_one("#code-view").scroll_home(animate=False)
      self.sub_title = event.path

  def action_toggle_files(self) -> None:
    """Called in response to key binding."""
    self.show_tree = not self.show_tree

def telnet():
  return "Some software is included in the Taser suite and only works on a local computer. " \
         "This programme is included in the Taser suite"


def main():
  CodeBrowser().run()


