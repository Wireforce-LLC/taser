from prettytable import PrettyTable

from sdk.manifest import read_permissions, read_activities
from sdk.require_android_path import require_android_manifest_path


def main():
    table = PrettyTable()
    table._max_width = {"Activity": 45, "isMain": 5}
    table.field_names = ["Activity", "isMain"]
    table.align["Activity"] = "l"
    table.align["isMain"] = "l"
    table.padding_width = 2

    path = require_android_manifest_path()

    if path:
        activities = read_activities(path)

        for activity in activities:

            table.add_row([
                activity.get('name', "N/A"),
                activity.get('isMain', "N/A")
            ])

        return table

    else:
        return f"path ({path}) is not a android dir"