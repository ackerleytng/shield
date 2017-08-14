import __builtin__
import common

import os


PREFIX = "builtin_"
ORIGINAL_MODULE = __builtin__
HOOKS = {
    "open": None
}


def builtin_open(name, mode="r", buffering=-1):
    original_open = HOOKS["open"]
    assert original_open is not None

    if mode.startswith("r"):
        return original_open(name, mode, buffering)
    elif mode.startswith("w"):
        path = os.path.abspath(name)
        if common.is_in_safe_directories(path):
            return original_open(path, mode, buffering)
        else:
            raise common.ShieldError("You shouldn't "
                                     "be writing to {}!".format(path))
    else:
        # Otherwise, some weird mode is requested,
        #   let python's open handle it
        return original_open(name, mode, buffering)
