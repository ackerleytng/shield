import os
import sys
import tempfile


def running_on_windows():
    return sys.platform.startswith("win")


def running_in_cygwin():
    return running_on_windows() and os.environ.get("CYGWIN_VERSION", False)

def running_on_linux():
    return sys.platform.startswith("linux")


def running_on_mac():
    return sys.platform.startswith("darwin")


def get_desktop_path():
    if running_on_windows():
        # Because expanduser in cygwin does not point to Windows' home
        user_profile = os.environ.get("USERPROFILE", None)
        if user_profile is None:
            raise NotImplementedError("Couldn't find path to Desktop!")

        path = os.path.join(user_profile, "Desktop")
    else:
        path = os.path.expanduser("~/Desktop")

    if not os.path.exists(path):
        raise NotImplementedError("Couldn't find path to Desktop!")

    return path


def get_temp_path():
    return tempfile.gettempdir()


SAFE_DIRECTORIES = [get_desktop_path(), get_temp_path()]


def add_safe_directory(path):
    SAFE_DIRECTORIES.append(os.path.abspath(path))


def write_check(mode):
    # perhaps a check can be done here to allow writing in some places
    # i.e not totally no writing, but to only to allowed files
    # can be totally no writing for now
    if "w" in mode:
        print "No writing!"


def split_path(abspath):
    """Takes an absolute path and splits it up.

    Returns (drive, path split into parts)

    drive is only not "" on Windows systems.

    This site explains the massive inconsistency on Windows:
    https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python
    and so we're using the technique described there

    (On Windows)
    given: r'C:\Users\john\Desktop\foo\bar.txt'
    expect: ("C:", ["Users", "john", "Desktop", "foo", "bar.txt"])

    (On Linux)
    given: '/tmp/foo/bar.txt'
    expect: ("", ["tmp", "foo", "bar.txt"])
    """
    drive, path = os.path.splitdrive(abspath)

    parts = []
    while True:
        path_in = path
        path_out, tail = os.path.split(path_in)
        parts.append(tail)

        if path_in == path_out:
            parts.append(path_out)
            break

        path = path_out

    # Filter empty parts
    parts = [p for p in parts if p != '']

    return (drive, list(reversed(parts)))


def list_startswith(a, b):
    """Returns True if a starts with b and False otherwise

    given: a = [0, 1, 2], b = [0, 1, 2]
    expect: True

    given: a = [0, 1, 2, 3], b = [0, 1, 2]
    expect: True

    given: a = [0, 1, 3], b = [0, 1, 2]
    expect: False

    given: a = [0, 1], b = [0, 1, 2]
    expect: False
    """
    return (len(b) <= len(a) and
            a[:len(b)] == b)


def is_in_directory(path, path_to_directory):
    """Returns True if path is in the directory pointed to by path_to_directory
    and False otherwise

    Assumes that path_to_directory points to a directory
    """

    path_drive, path_parts = split_path(path)
    directory_drive, directory_parts = split_path(path_to_directory)

    return (path_drive == directory_drive and
            list_startswith(path_parts, directory_parts))


def is_in_safe_directories(path):
    """Returns True if path is in a 'safe' directory, where safe means

    it is either in the temp directory of a system
    or on the desktop of a system
    """
    abspath = os.path.abspath(path)
    safe_paths = [os.path.abspath(p) for p in SAFE_DIRECTORIES]

    return any([is_in_directory(abspath, d) for d in safe_paths])


def is_safe_for_writing(path):
    """Determines if a path is a safe path to write to

    A path is considered safe if it is
      ((in the temp directory on a system or
        on the desktop of a system) and
        if it is a file, it does not already exist)
    """
    abspath = os.path.abspath(path)

    return (is_in_safe_directories(path) and
            not os.path.isfile(abspath))


def make_unique(path):
    """Given a path, if the path already exists,
    prepend u- to it so that it is unique.
    If the path does not already exist, return it.

    Return the path, made unique.
    """
    while os.path.exists(path):
        drive, path = split_path(path)
        path[-1] = "u-" + path[-1]
        path = os.path.join(drive, *path)

    return path


class ShieldError(Exception):
    def __init__(self, *args, **kwargs):
        super(ShieldError, self).__init__(*args, **kwargs)


def disable_with_shielderror(string):
    def aux(*arg):
        raise ShieldError(string)
    return aux
