import os


def shield_open(name, mode="r", buffering=-1):
    print "Halt! Doing open"
    print name, mode, buffering


def shield_os_open(name, flags=os.O_RDONLY, mode=0777):
    print "Halt! Doing open"
    print name, flags, mode


def shield_remove(path):
    print "Halt! Doing remove"
    print path


def shield_rmdir(path):
    print "Halt! Doing rmdir"
    print path


def shield_removedirs(path):
    print "Halt! Doing removedirs"
    print path
