import os


def os_open(name, flags=os.O_RDONLY, mode=0777):
    print "Halt! Doing open"
    print name, flags, mode


def os_remove(path):
    print "Halt! Doing remove"
    print path


def os_rmdir(path):
    print "Halt! Doing rmdir"
    print path


def os_removedirs(path):
    print "Halt! Doing removedirs"
    print path


def do_hook():
    import os

    os.open = os_open
    os.remove = os_remove
    os.rmdir = os_rmdir
    os.removedirs = os_removedirs
