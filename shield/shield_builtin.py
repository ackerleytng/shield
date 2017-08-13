def builtin_open(name, mode, buffering=-1):
    print "Halt! Doing open"
    print name, mode, buffering


def do_hook():
    import __builtin__

    __builtin__.open = builtin_open
