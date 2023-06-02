import os
import tempfile
from os import path

_temp_dir = tempfile.gettempdir()


def read_taser_pwd():
    """
    Reads the content of the ".taser_pwd" file in the temporary directory.
    If the file exists, its content is returned after stripping any leading/trailing whitespace.
    If the file doesn't exist, it creates the file with the default value "~" and returns "~".
    Returns:
        The content of the ".taser_pwd" file or "~" if the file doesn't exist.
    """

    file_path = os.path.join(_temp_dir, ".taser_pwd")

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    else:
        with open(file_path, 'w') as file:
            file.write("~")
        return "~"


def write_taser_pwd(data):
    """
    Writes the provided data to the ".taser_pwd" file in the temporary directory.
    Args:
      data: The data to be written to the file.
    """

    file_path = os.path.join(_temp_dir, ".taser_pwd")

    with open(file_path, 'w') as file:
        file.write(data)


def format_cp():
    """
    Returns the last component of the path obtained from reading the ".taser_pwd" file.
    Returns:
        The last component of the path or an empty string if the path is empty.
    """

    return path.split(get_cp())[-1]


def get_cp():
    """
    Returns the normalized and real path obtained from reading the ".taser_pwd" file.
    Returns:
       The normalized and real path from the ".taser_pwd" file.
    """
    return path.normpath(path.realpath(read_taser_pwd()))


def set_cp(cp):
    """
    Sets the provided path as the new value in the ".taser_pwd" file.
    Args:
        cp: The new path value.
    Returns:
        The absolute, normalized, and real path after setting the new value in the ".taser_pwd" file.
        Returns False if the provided path is not a directory or if it is an empty directory.
    """

    if not path.isdir(cp):
        return False

    if not os.listdir(cp):
        return False

    if " " in cp:
        print("WARNING!! Your folder contains spaces. Some plugins may not work correctly")

    path_to = path.abspath(path.normpath(path.realpath(cp)))

    write_taser_pwd(path_to)

    return path_to
