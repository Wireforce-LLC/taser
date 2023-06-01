def main(prism_report: dict = None):
  if hasattr(globals(), "__prism_map_index__") and not prism_report:
    prism_report = globals()['__prism_map_index__']

  graphs = prism_report.get('nav_graphs_fragments', {})
  xml_colors = prism_report.get("colors_xml", {}).values()

  x_activity = len(prism_report.get('activities', [])) / 3

  count_permissions = len(prism_report.get('permissions', []))
  count_fragments = 0

  if count_permissions > 0:
    x_permissions = 1 / count_permissions

  else:
    x_permissions = 0.5

  token_count = prism_report.get('tokenize', {}).get("count_tokens", 0)
  x_tokens = token_count / 1250

  strings_xml_values = prism_report.get('strings_xml', {}).values()
  x_string = len(strings_xml_values) * 0.005

  libs_stack = prism_report.get('libs_stack', [])
  libs_stack_weights = sum(list(map(lambda x: x.get('lib', {}).get('weight', 0), libs_stack)))
  x_libs_stack_weights = libs_stack_weights

  if graphs:
    for graph in graphs:
      if not graphs[graph]:
        continue

      count_fragments = count_fragments + len(graphs[graph])

  x_revisoro = prism_report.get('revisoro_percent', 0) / 140

  x_fragments = count_fragments / 3

  y_color = 0
  y_tokenize_ratio_anomaly = 0
  y_big_file_lines = 0

  if prism_report.get('tokenize', {}).get("is_significant_anomaly", False):
    y_tokenize_ratio_anomaly = prism_report.get('tokenize', {}).get("ratio_anomaly", 0) / 10

  if "#FFBB86FC" in xml_colors:
    y_color = y_color + 0.05

  if "#FF6200EE" in xml_colors:
    y_color = y_color + 0.06

  if "#FF3700B3" in xml_colors:
    y_color = y_color + 0.06

  if "#FF03DAC5" in xml_colors:
    y_color = y_color + 0.06

  if "#FF018786" in xml_colors:
    y_color = y_color + 0.06

  y_big_files_list = prism_report.get('tokenize', {}).get("files_lines", [])

  for file in y_big_files_list:
    # 2500 * 1.8/2500
    y_big_files = y_big_files_list[file]

    if y_big_files > 2500:
      xy = y_big_files * (y_big_files / 2500 * 0.6) / 2500
      y_big_file_lines = y_big_file_lines + xy

  score = x_activity + x_fragments + x_tokens + x_string + x_permissions + x_libs_stack_weights
  fine = y_color + x_revisoro + y_tokenize_ratio_anomaly + y_big_file_lines

  return {
    "score": round(score - fine, 4),
    "fine": round(fine, 4),
    "fine_x": {
      "x_revisoro": round(x_revisoro, 2),
      "y_color": round(y_color, 2),
      "y_big_file_lines": round(y_big_file_lines, 2),
      "y_tokenize_ratio_anomaly": round(y_tokenize_ratio_anomaly, 2)
    },
    "score_x": {
      "x_activity": round(x_activity, 2),
      "x_fragments": round(x_fragments, 2),
      "x_tokens": round(x_tokens, 2),
      "x_string": round(x_string, 2),
      "x_permissions": round(x_permissions, 2),
      "x_libs_stack_weights": round(x_libs_stack_weights, 2)
    }
  }
