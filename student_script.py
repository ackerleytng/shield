import shield
import os
import io

open("/dummy_folder",'r')

os.open("/dev/null", os.O_RDONLY)

os.remove("/dummy_folder")

os.rmdir("/dummy_folder")

os.removedirs("/dummy_folder")

with io.open("test.txt", 'w') as f:
    print f.write(u"adasd")
