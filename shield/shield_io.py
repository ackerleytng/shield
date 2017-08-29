import io
import os
import common

PREFIX = "io_"
ORIGINAL_MODULE = io
HOOKS = {
    "open": None,
    "FileIO": None,
}
ORIGINALS = {}


def io_open(file_, mode='r', buffering=-1, encoding=None,
            errors=None, newline=None, closefd=True):
    original_open = ORIGINALS["open"]
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


# Replacing the entire class with a subclassed version that checks inputs
class io_FileIO(io.FileIO):
    def __init__(self, name, mode='r', closefd=True):
        if (type(name) != str or
            type(mode) != str or
            type(closefd) != bool):
            return super(io_FileIO, self).__init__(name, mode, closefd)
        elif ("w" in mode or
              "a" in mode or
              "+" in mode):
            path = os.path.abspath(name)
            if common.is_in_safe_directories(path):
                return super(io_FileIO, self).__init__(path, mode, closefd)
            else:
                raise common.ShieldError("You shouldn't "
                                         "be writing to {}!".format(path))
        else:
            return super(io_FileIO, self).__init__(name, mode, closefd)
