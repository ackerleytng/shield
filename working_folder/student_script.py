from protected import protected
import os
proc = protected.protected_class()

proc.protected_open("/dev/null", "r", -1)

os.open("/dev/null", "r", -1)

os.remove("/dummy_folder")

os.rmdir("/dummy_folder")

os.removedirs("/dummy_folder")


