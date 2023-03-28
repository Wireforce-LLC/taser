from xml.dom.minidom import parseString

from sdk.require_android_path import require_android_manifest_path

def get_package_name(manifest: str = require_android_manifest_path()):
  pass

def read_permissions(manifest: str = require_android_manifest_path()):
    data = ''  # string data from file
    perms_list = []

    with open(manifest, 'r') as f:
        data = f.read()
        dom = parseString(data)  # parse file contents to xml dom
        nodes = dom.getElementsByTagName('uses-permission')  # xml nodes named "uses-permission"
        nodes += dom.getElementsByTagName('uses-permission-sdk-23')  # xml nodes named "uses-permission-sdk-23"
        permissions = []  # holder for all permissions as we gather them
        # Iterate over all the uses-permission nodes
        for node in nodes:
            permissions += [node.getAttribute("android:name")]  # save permissionName to our list
        # Print sorted list
        for permission in sorted(permissions):  # sort permissions and iterate
            perms_list.append(permission)  # print permission name

    return perms_list


def read_activities(manifest: str = require_android_manifest_path()):
    activities_list = []

    data = ''
    with open(manifest, 'r') as f:
        data = f.read()
        dom = parseString(data)
        activities = dom.getElementsByTagName('activity')

        for activity in activities:
            isMain = False
            name = activity.getAttribute('android:name')
            intents = activity.getElementsByTagName('intent-filter')
            for intent in intents:
                actions = intent.getElementsByTagName('action')
                for action in actions:
                    if  action.getAttribute('android:name') == 'android.intent.action.MAIN':
                        isMain = True

            activities_list.append({
                "name": name,
                "isMain": isMain
            })

    return activities_list