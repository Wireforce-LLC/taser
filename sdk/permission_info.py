import json


with open('./sdk/android_permissions_list.json', 'r') as file:
  pemissions_info = json.loads(file.read())

  file.close()

def get_permission_info(permission: str):
    return pemissions_info.get('permissions', {}).get(permission, {})