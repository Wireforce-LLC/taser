import requests

PROMPT_TOOLKIT_ARGS = ""

def main(data):

  for d in data:
    g = d['g']
    pgk = d['pgk']
    version = d['version']

    url = f"https://search.maven.org/solrsearch/select?q=g:{g}+AND+a:{pgk}&core=gav&rows=20&wt=json"
    response = requests.get(url)
    json_data = response.json()

    d['latest_version'] = None

    if json_data['response']['docs']:
      latest_version = json_data['response']['docs'][0]['v']

      d['latest_version'] = latest_version

  return data