import shield
# import os
# import io


try:
    with open("student_script.py", 'w') as f:
        print f.read()
except shield.common.ShieldError:
    print "Correctly shielded!"

test = something

"""
os.open("/dev/null", os.O_RDONLY)

os.remove("/dummy_folder")

os.rmdir("/dummy_folder")

os.removedirs("/dummy_folder")

with io.open("test.txt", 'w') as f:
    print f.write(u"adasd")
"""
