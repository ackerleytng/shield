import os
import sys
import tempfile


def write_check(mode):
    # perhaps a check can be done here to allow writing in some places
    # i.e not totally no writing, but to only to allowed files
    # can be totally no writing for now
    if "w" in mode:
        print "No writing!"


def running_on_windows():
    return sys.platform.startswith("win")


def running_on_linux():
    return sys.platform.startswith("linux")


def running_on_mac():
    return sys.platform.startswith("darwin")


def get_desktop_path():
    path = os.path.expanduser("~/Desktop")

    if not os.path.exists(path):
        raise NotImplementedError("Couldn't find path to Desktop!")

    return path


def get_temp_path():
    return tempfile.gettempdir()


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
        if path_in == path_out:
            break
        path = path_out
        parts.append(tail)

    # Filter empty parts
    parts = [p for p in parts if p != '']

    return (drive, list(reversed(parts)))


def is_safe(path):
    """Determines if a path is a safe path to write to

    A path is considered safe if it is a new directory
    + in the temp directory on a system
    + on the desktop of a system
    """
    pass
