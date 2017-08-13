import __builtin__


PREFIX = "builtin_"
ORIGINAL_MODULE = __builtin__
HOOKS = (
    "open",
)


def builtin_open(name, mode='r', buffering=-1):
    print "Halt! Doing open"
    print name, mode, buffering
