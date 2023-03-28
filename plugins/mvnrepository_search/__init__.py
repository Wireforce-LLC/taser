import re
import requests

from bs4 import BeautifulSoup

def main(implementation):
  url = 'https://mvnrepository.com/artifact/androidx.constraintlayout/constraintlayout'

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
  }

  html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(html, 'html.parser')

  print(html)

  return soup.find(_class="vbtn")

      # dependencies_array.append({
      #   'g': groups.group('g'),
      #   'pgk': groups.group('pgk'),
      #   'version': groups.group('version')
      # })
