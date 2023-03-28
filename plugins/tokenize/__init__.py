import os.path
import re

import plugins.source_map
from nltk.probability import FreqDist

def main():
  files = plugins.source_map.main("read")

  if isinstance(files, str):
    return files

  count_all_tokens = 0
  file_to_tokens = {}

  count_all_lines = 0
  file_to_lines = {}

  for file in files:
    if not os.path.isfile(file):
      continue

    content = open(file, 'r').read()

    if content:
      tokens = len(re.findall(r'\w+', content))
      lines = len(list(filter(lambda item: item, content.split("\n"))))

      count_all_tokens = count_all_tokens + tokens
      file_to_tokens[file] = tokens

      count_all_lines = count_all_lines + lines
      file_to_lines[file] = lines

  return {
    "count_tokens": count_all_tokens,
    "count_all_lines": count_all_lines,
    "ratio_anomaly": count_all_tokens / count_all_lines,
    "is_significant_anomaly": (count_all_tokens / count_all_lines) > 8.,
    "files_tokens": file_to_tokens,
    "files_lines": file_to_lines
  }


