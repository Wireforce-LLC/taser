from sdk.manifest import read_permissions
from sdk.permission_info import get_permission_info
from sdk.require_android_path import require_android_manifest_path, require_android_strings_xml_path
from prettytable import PrettyTable

from sdk.strings import get_strings


def main():
    table = PrettyTable()
    table._max_width = {"Name" : 30, "Value" : 50}

    table.field_names = ["Name", "Value"]
    table.align["Name"] = "l"
    table.align["Value"] = "l"
    table.padding_width = 2

    path = require_android_strings_xml_path()

    if path:
        strings = get_strings(path)

        for string in strings:
            table.add_row([
              strings[string],
              string,
            ])

        return table

    else:
        return f"path ({path}) is not a android dir"