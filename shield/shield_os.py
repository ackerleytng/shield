import os
import common


PREFIX = "os_"
ORIGINAL_MODULE = os
HOOKS = {
    "open": None,
}


def os_open(name, flags, mode=0777):
    original_open = HOOKS["open"]
    assert original_open is not None

    if type(name) != str or type(flags) != int or flags == os.O_RDONLY:
        return original_open(name, flags, mode)
    elif any([flags & f for f in [os.O_WRONLY,
                                  os.O_RDWR,
                                  os.O_APPEND,
                                  os.O_CREAT,
                                  os.O_TRUNC]]):
        path = os.path.abspath(name)
        if common.is_in_safe_directories(path):
            return original_open(path, flags, mode)
        else:
            raise common.ShieldError("You shouldn't "
                                     "be writing to {}!".format(path))
    else:
        # Something is really weird
        return original_open(name, flags, mode)


def os_remove(path):
    print "Halt! Doing remove"
    print path


def os_rmdir(path):
    print "Halt! Doing rmdir"
    print path


def os_removedirs(path):
    print "Halt! Doing removedirs"
    print path
