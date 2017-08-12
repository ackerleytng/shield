from protected import protected
import os

import io


proc = protected.protected_class()

proc.protected_open("/dev/null", "r", -1)

os.open("/dev/null", "r", -1)

os.remove("/dummy_folder")

os.rmdir("/dummy_folder")

os.removedirs("/dummy_folder")

with io.open("test.txt", 'w') as f:
    print f.write(u"adasd")
