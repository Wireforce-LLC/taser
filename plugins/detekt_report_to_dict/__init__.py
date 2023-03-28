import xml.etree.ElementTree as ET


def main(path: str):
  tree = ET.parse(path)
  root = tree.getroot()

  d = {}

  for x in root.findall('file'):
    for e in x.findall("error"):
      if not x.attrib['name'] in d.keys():
        d[x.attrib['name']] = []

      d[x.attrib['name']].append(
        {
          "line": e.attrib['line'],
          "column": e.attrib['column'],
          "severity": e.attrib['severity'],
          "message": e.attrib['message'],
        }
      )

  return d