def io_open(name, mode, buffering=-1):
    print "Halt! Doing open"
    print name, mode, buffering


def do_hook():
    import io

    io.open = io_open
