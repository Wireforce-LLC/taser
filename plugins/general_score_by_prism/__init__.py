import random

# Formula
# x_activity = {count_activity} / 3
# x_impl = 1 - {old_impl_count} / {all_impl}
# x_tokens = {x_tokens} / {avg_tokens}
# x_constrastnost = if Yes 1 else 0

def main(prism_report: dict = None):
  if hasattr(globals(), "__prism_map_index__") and not prism_report:
    prism_report = globals()['__prism_map_index__']

  fine = 0


  graphs = prism_report.get('nav_graphs_fragments', {})
  xml_colors = prism_report.get("colors_xml", {}).values()

  x_activity = len(prism_report.get('activities', [])) / 3

  count_permissions = len(prism_report.get('permissions', []))
  count_fragments = 0

  if count_permissions > 0:
    x_permissions = 3 / count_permissions

  else:
    x_permissions = 0.5

  x_tokens = prism_report.get('tokenize', {}).get("count_tokens", 0) / 1250
  x_string = len(prism_report.get('strings_xml', {}).values()) * 0.005
  x_libs_stack_weights = sum(list(map(lambda x: x.get('lib', {}).get('weight'), prism_report.get('libs_stack', []))))

  if graphs:
    for graph in graphs:
      if not graphs[graph]:
        continue

      count_fragments = count_fragments + len(graphs[graph])

  x_revisoro = prism_report.get('revisoro_percent', 0) / 140

  x_fragments = count_fragments / 3

  y_color = 0
  y_tokenize_ratio_anomaly = 0

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

  score = x_activity + x_fragments + x_tokens + x_string + x_permissions + x_libs_stack_weights
  fine = y_color + x_revisoro + y_tokenize_ratio_anomaly

  return {
    "score": round(score - fine, 4),
    "fine": round(fine, 4),
    "fine_x": {
      "x_revisoro": round(x_revisoro, 2),
      "y_color": round(y_color, 2),
      "y_tokenize_ratio_anomaly": round(y_tokenize_ratio_anomaly, 2)
    },
    "score_x": {
      "x_activity": round(x_activity, 2),
      "x_fragments": round(x_fragments, 2),
      "x_tokens": round(x_tokens, 2),
      "x_string": round(x_string, 2),
      "x_permissions": round(x_permissions, 2),
      "x_revisoro": round(x_revisoro, 2),
      "x_libs_stack_weights": round(x_libs_stack_weights, 2)
    }
  }
