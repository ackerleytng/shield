import os
import sys

def write_check(mode):
    # perhaps a check can be done here to allow writing in some places
    # i.e not totally no writing, but to only to allowed files
    # can be totally no writing for now
    if "w" in mode:
        print "No writing!"
        sys.exit()

def shield_open(name, mode, buffering=-1):
    write_check(mode)
    print "Halt! Doing open"
    print name, mode, buffering

def shield_io_open(name, mode, buffering=-1):
    write_check(mode)
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
