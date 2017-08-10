def my_open(name, mode=None, buffering=None):
    print name, mode, buffering

import __builtin__
saved_open = __builtin__.open
__builtin__.open = my_open
import os
os.open = my_open


print type(open("/dev/null", "r", -1))

import io
with io.open('spam.txt', 'w') as file:
    file.write(u'Spam and eggs!')

from zipfile import ZipFile
with ZipFile('spam.zip', 'w') as myzip:
    myzip.write('eggs.txt')
