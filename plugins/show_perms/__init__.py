from sdk.manifest import read_permissions
from sdk.permission_info import get_permission_info
from sdk.require_android_path import require_android_manifest_path
from prettytable import PrettyTable


def main():
    table = PrettyTable()
    table._max_width = {"Permission" : 30, "Description" : 45}

    table.field_names = ["Permission", "Description"]
    table.align["Permission"] = "l"
    table.align["Description"] = "l"
    table.padding_width = 2

    path = require_android_manifest_path()

    if path:
        perms = read_permissions(path)

        for perm in perms:
            permission_info = get_permission_info(perm)
            table.add_row([
                perm,
                permission_info.get('description', 'N/A').strip()
            ])

        return table

    else:
        return f"path ({path}) is not a android dir"