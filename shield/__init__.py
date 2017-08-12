import shield
import __builtin__
import os
import io


__builtin__.open = shield.shield_open
os.open = shield.shield_os_open
io.open = shield.shield_io_open
os.remove = shield.shield_remove
os.rmdir = shield.shield_rmdir
os.removedirs = shield.shield_removedirs
