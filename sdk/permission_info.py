import json


pemissions_info = json.loads(open('./sdk/android_permissions_list.json', 'r').read())

def get_permission_info(permission: str):
    return pemissions_info.get('permissions', {}).get(permission, {})