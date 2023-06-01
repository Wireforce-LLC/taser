import importlib
import pkgutil
import inspectors
from core.cp import get_cp


def iter_namespace(ns_pkg):
  # Specifying the second argument (prefix) to iter_modules makes the
  # returned name an absolute name instead of a relative one. This allows
  # import_module to work without having to do additional modification to
  # the name.
  return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

discovered_inspectors = {}

def init():
  inspectors.discovered_inspectors = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(inspectors)
  }


def start_inspector(name: str, path: str = get_cp(), meta = {}):
  inspector_name = f"inspectors.{name}"

  if inspector_name in discovered_inspectors.keys():
    inspector_obj = discovered_inspectors[inspector_name]
    if hasattr(inspector_obj, "test"):
      return inspector_obj.test(path, meta)

  return False