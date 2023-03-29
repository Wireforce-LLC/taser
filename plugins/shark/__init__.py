from bson import SON
from pydash import group_by
from rich.syntax import Syntax
from textual import events
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.reactive import reactive
from textual.widgets import Header, Footer, DirectoryTree, Static, Tree, Label, ListItem, ListView
from textual.widgets._tree import TreeNode, EventTreeDataType

import inspectors.hybrid_autotest
from executor import is_telnet

PROMPT_TOOLKIT_ARGS = ""

PROMPT_WELCOME = "🦈 Shark is a client for searching reports in the database.\n" \
                 "Works both with the local version of taser and via telnet"


mongo_docs = inspectors.hybrid_autotest.mongo_docs.docs


class ListViewApp(App):
  CSS_PATH = "list_view.css"

  def compose(self) -> ComposeResult:
    tree: Tree[dict] = Tree("Root")
    groups = group_by(list(mongo_docs.find({})), "meta.sender_id")

    for item in groups:
      branch = tree.root.add(str(item))

      for i in groups[item]:
        branch.add(i.get('vpath'), data=i.get('vpath'))

    yield tree

  def on_tree_node_selected(self, item: TreeNode[EventTreeDataType]):
    if item.node.data:
      self.exit(item.node.data)


def telnet(pipeline, mode="find"):
  if mode == "aggregate":
    return list(
      mongo_docs.aggregate(pipeline)
    )

  elif mode == "find":
    return mongo_docs.find(pipeline)


def main(arg, meta={}):
  if arg == "select_path" and not is_telnet:
    return ListViewApp().run()

  elif arg == "aggregate":
    return list(
      mongo_docs.aggregate(meta)
    )

  elif arg == "find":
    return mongo_docs.find(meta)
