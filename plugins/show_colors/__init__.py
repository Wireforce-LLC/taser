from PIL import ImageColor
from prettytable import PrettyTable
from rich.console import Console
from rich.panel import Panel

from sdk.require_android_path import require_android_colors_xml_path
from sdk.theme import get_colors

DEFAULT_NEW_PROJECT_COLORS = [
  (255, 187, 134, 252),
  (255, 98, 0, 238),
  (255, 55, 0, 179),
  (255, 3, 218, 197),
  (255, 1, 135, 134),
]


def hex_to_rgb(hex_value):
  h = hex_value.lstrip('#')
  return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
  return '%02x%02x%02x' % rgb


def rgb_255_to_hex(rgb: list):
  if len(rgb) == 4:
    return '%02x%02x%02x' % (rgb[1], rgb[2], rgb[3])

  if len(rgb) == 3:
    return '%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

def main(tkinter=False):
  import tkinter as tk

  class ColorChart(tk.Frame):
    MAX_ROWS = 36
    FONT_SIZE = 10

    def __init__(self, root, colors):
      tk.Frame.__init__(self, root)
      r = 0
      c = 0

      for color in colors:
        label = tk.Label(self, text=color, bg=color[0:7])
        label.grid(row=r, column=c, sticky="ew")
        r += 1

        if r > self.MAX_ROWS:
          r = 0
          c += 1

      self.pack(expand=1, fill="both")

  table = PrettyTable()
  table._max_width = {"Name": 30, "Value": 50}

  table.field_names = ["Name", "Value"]
  table.align["Name"] = "l"
  table.align["Value"] = "l"

  table.padding_width = 2

  path = require_android_colors_xml_path()

  if path:
    colors = get_colors(path)

    if tkinter:
      root = tk.Tk()
      root.title("Named Color Chart")
      app = ColorChart(root, colors.values())
      root.mainloop()

    lines = []

    for color in colors:
      if not tkinter:
        rgb = ImageColor.getrgb(colors[color])

        line = "{:>12} {:>25} {:>12} {:>5}".format(
          color,
          str(rgb),
          f" [#{rgb_255_to_hex(rgb)}]███████ ",
          f"[#ffffff] Default: {rgb in DEFAULT_NEW_PROJECT_COLORS}"
        )

        lines.append(line)

      table.add_row([
        color,
        colors[color]
      ])

    if lines:
      Console().print()
      Console().print(
        Panel.fit("\n".join(lines), title="Colors Preview")
      )
      Console().print()

    return table

  else:
    return f"path ({path}) is not a android dir"
