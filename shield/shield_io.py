import io
import os
import common

PREFIX = "io_"
ORIGINAL_MODULE = io
HOOKS = {
    "open": None,
}


def io_open(file_, mode='r', buffering=-1, encoding=None,
            errors=None, newline=None, closefd=True):
    original_open = HOOKS["open"]
    assert original_open is not None

    if (type(file_) != str or
        type(mode) != str or
        type(buffering) != int or
        (encoding is not None and type(encoding) != str) or
        (errors is not None and type(errors) != str) or
        (newline is not None and type(newline) != str) or
        type(closefd) != bool):
        return original_open(file_, mode, buffering, encoding,
                             errors, newline, closefd)
    elif ("w" in mode or
          "a" in mode or
          "+" in mode):
        path = os.path.abspath(file_)
        if common.is_in_safe_directories(path):
            return original_open(path, mode, buffering, encoding,
                                 errors, newline, closefd)
        else:
            raise common.ShieldError("You shouldn't "
                                     "be writing to {}!".format(path))
    else:
        # Otherwise, some weird mode is requested,
        #   let python's open handle it
        return original_open(file_, mode, buffering, encoding,
                             errors, newline, closefd)
