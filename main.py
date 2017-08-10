def my_open(name, mode=None, buffering=None):
    print name, mode, buffering

import __builtin__
saved_open = __builtin__.open
__builtin__.open = my_open


print type(open("/dev/null", "r", -1))
