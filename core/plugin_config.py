import yaml

plugin_configs = {}

with open("data/plugins.yml", 'r') as document:
  plugin_configs = yaml.safe_load(document)


def get_plugin_config(plugin: str):
  return plugin_configs.get(plugin, None)