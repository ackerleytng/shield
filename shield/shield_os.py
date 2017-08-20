import os
import common


PREFIX = "os_"
ORIGINAL_MODULE = os
HOOKS = {
    "open": None,
    "chroot": None,
    "chflags": None,
    "lchflags": None,
    "chmod": None,
    "lchmod": None,
    "chown": None,
    "lchown": None,
    "link": None,
    "mknod": None,
    "mkfifo": None,
    "makedev": None,
}


def os_open(name, flags, mode=0777):
    original_open = HOOKS["open"]
    assert original_open is not None

    if type(name) != str or type(flags) != int or flags == os.O_RDONLY:
        return original_open(name, flags, mode)
    elif any([flags & f for f in [os.O_WRONLY,
                                  os.O_RDWR,
                                  os.O_APPEND,
                                  os.O_CREAT,
                                  os.O_TRUNC]]):
        path = os.path.abspath(name)
        if common.is_in_safe_directories(path):
            return original_open(path, flags, mode)
        else:
            raise common.ShieldError("You shouldn't "
                                     "be writing to {}!".format(path))
    else:
        # Something is really weird
        return original_open(name, flags, mode)


"""
os.fdopen is not guarded because fdopen takes a file descriptor,
  which first has to be opened by os.open.
The mode of fdopen must match what it was os.opened with, so there
  shouldn't be a chance of fdopen being used for write when it wasn't
  opened in the write mode
This applies for all the other functions that take an fd, such as

+ os.fdatasync
+ os.fsync
+ os.ftruncate
+ os.write
+ os.fchmod
"""


def _os_chmod(function_name, present_participle):
    def aux(path, mode):
        original_function = HOOKS[function_name]
        assert original_function is not None

        if type(path) != str or type(mode) != int:
            return original_function(path, mode)
        else:
            abspath = os.path.abspath(path)
            if common.is_in_safe_directories(abspath):
                return original_function(abspath, mode)
            else:
                msg = "You shouldn't be {} in {}!".format(present_participle,
                                                          abspath)
                raise common.ShieldError(msg)
    return aux


os_chmod = _os_chmod("chmod", "chmoding")
os_lchmod = _os_chmod("lchmod", "lchmoding")


def _os_chown(function_name, present_participle):
    def aux(path, uid, gid):
        original_function = HOOKS[function_name]
        assert original_function is not None

        if type(path) != str or type(uid) != int or type(gid) != int:
            return original_function(path, uid, gid)
        else:
            abspath = os.path.abspath(path)
            if common.is_in_safe_directories(abspath):
                return original_function(abspath, uid, gid)
            else:
                msg = "You shouldn't be {} in {}!".format(present_participle,
                                                          abspath)
                raise common.ShieldError(msg)
    return aux


os_chown = _os_chown("chown", "chowning")
os_lchown = _os_chown("lchown", "lchowning")


# Don't think beginners would need to use these
os_chflags = common.disable_with_shielderror(
    "Are you sure you need to use chflags?")
os_lchflags = common.disable_with_shielderror(
    "Are you sure you need to use lchflags?")
os_chroot = common.disable_with_shielderror(
    "Are you sure you need to use chroot?")
os_mkfifo = common.disable_with_shielderror(
    "Are you sure you need to use mkfifo?")
os_mknod = common.disable_with_shielderror(
    "Are you sure you need to use mknod?")
os_makedev = common.disable_with_shielderror(
    "Are you sure you need to use makedev?")


def os_link(source, link_name):
    original_function = HOOKS["link"]
    assert original_function is not None

    if type(source) != str or type(link_name) != str:
        return original_function(source, link_name)
    else:
        abspath = os.path.abspath(link_name)
        if common.is_in_safe_directories(abspath):
            return original_function(source, link_name)
        else:
            msg = "You shouldn't be linking to {}!".format(abspath)
            raise common.ShieldError(msg)


def os_remove(path):
    print "Halt! Doing remove"
    print path


def os_rmdir(path):
    print "Halt! Doing rmdir"
    print path


def os_removedirs(path):
    print "Halt! Doing removedirs"
    print path
