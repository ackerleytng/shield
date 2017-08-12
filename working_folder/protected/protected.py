import sys
# Overwriting functions with protected ones
class protected_class:
    def __init__(self):
        import __builtin__
        __builtin__.open = self.protected_open
        import os
        os.open = self.protected_open
        os.remove = self.protected_remove
        os.rmdir = self.protected_rmdir
        os.removedirs = self.protected_removedirs
        import io
        io.open = self.protected_io_open
    
    def protected_open(self, name, mode=None, buffering=None):
        print "Halt! Calling modified open"
        print name, mode, buffering

    def protected_io_open(self, name, mode, encoding=None, buffering=None):
        if 'w' in mode:
            print "No writing allowed!"
            sys.exit()
        else:
            io.open(name,mode)
            print name, mode, buffering

    def protected_remove(self, path):
        print "Halt! Doing remove"
        print path

    def protected_rmdir(self, path):
        print "Halt! Doing rmdir"
        print path

    def protected_removedirs(self, path):
        print "Halt! Doing removedirs"
        print path




