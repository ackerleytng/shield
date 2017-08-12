import __builtin__
saved_open = __builtin__.open
saved_import = __builtin__.__import__


def my_open(name, mode=None, buffering=None):
    print "my_open", name, mode, buffering


def my_import(name, globals_=None, locals_=None, fromlist=(), level=0):
    print "my_import", name
    saved_import(name, globals_, locals_, fromlist, level)


__builtin__.open = my_open
# __builtin__.__import__ = my_import


import os

os.open = my_open

print type(open("/dev/null", "r", -1))

print "os.open", os.open("test")

import stuff

with stuff.zzzz('spam.txt') as file:
    file.write(u'Spam and eggs!')

from zipfile import ZipFile
with ZipFile('spam.zip', 'w') as myzip:
    myzip.write('eggs.txt')
