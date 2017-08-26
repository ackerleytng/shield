import os
import stat
import traceback
import pytest
import shield


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, os.O_RDONLY, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, os.O_RDONLY, None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
     None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
     None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_APPEND,
     None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_APPEND,
     None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True,
     os.O_WRONLY | os.O_CREAT | os.O_APPEND,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True,
     os.O_RDWR | os.O_CREAT | os.O_TRUNC,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True,
     os.O_RDWR | os.O_CREAT | os.O_APPEND,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, os.O_RDWR,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, None, TypeError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, "x", TypeError),
])
def os_open_fixture(request):
    created_file = False
    path, should_create, flags, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (path, flags, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file:
        os.remove(path)


def test_os_open(os_open_fixture):
    path, flags, expected_exception = os_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            fd = os.open(path, flags)
    else:
        fd = os.open(path, flags)

    os.close(fd)


@pytest.mark.parametrize("disabled_call", [
    lambda: os.chflags("/tmp/stuff", stat.SF_IMMUTABLE),
    lambda: os.chroot("/tmp/stuff"),
    lambda: os.lchflags("/tmp/stuff", stat.SF_IMMUTABLE),
    lambda: os.mkfifo("/tmp/stuff"),
    lambda: os.mkfifo("/tmp/stuff", 0666),
    lambda: os.mknod("/tmp/stuff"),
    lambda: os.mknod("/tmp/stuff", 0666, 0),
    lambda: os.makedev(5, 5),
    lambda: os.pathconf("/tmp/stuff", "PC_FILESIZEBITS"),
    lambda: os.removedirs("/tmp/stuff"),
    lambda: os.renames("/tmp/stuff", "/tmp/other-stuff"),
    lambda: os.utime("/tmp/stuff", None),
])
def test_disabled(disabled_call):
    shield.install_hooks()
    try:
        # With this try-except, other errors will be caught
        #   and hooks will still be uninstalled
        with pytest.raises(shield.common.ShieldError):
            disabled_call()
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, stat.S_IWRITE, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, stat.S_IWRITE, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, stat.S_IWRITE,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, None, TypeError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, "x", TypeError),
])
def os_chmod_fixture(request):
    created_file = False
    path, should_create, mode, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (path, mode, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file:
        os.remove(path)


def test_os_chmod(os_chmod_fixture):
    path, mode, expected_exception = os_chmod_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.chmod(path, mode)
    else:
        os.chmod(path, mode)


def test_os_lchmod(os_chmod_fixture):
    path, mode, expected_exception = os_chmod_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.lchmod(path, mode)
    else:
        os.lchmod(path, mode)


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, -1, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, -1, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, -1,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, None, TypeError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, "x", TypeError),
])
def os_chown_fixture(request):
    created_file = False
    path, should_create, id_, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (path, id_, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file:
        os.remove(path)


def test_os_chown(os_chown_fixture):
    path, id_, expected_exception = os_chown_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.chown(path, id_, id_)
    else:
        os.chown(path, id_, id_)


def test_os_lchown(os_chown_fixture):
    path, id_, expected_exception = os_chown_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.lchown(path, id_, id_)
    else:
        os.lchown(path, id_, id_)


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"),
     True,
     os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-link.txt"),
     None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"),
     True,
     os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-link.txt"),
     None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"),
     True,
     os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-link.txt"),
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"),
     False, 1, TypeError),
    (0, False, 1, TypeError),
])
def os_link_fixture(request):
    created_file = False
    source, should_create, link_name, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(source)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (source, link_name, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if expected_exception is None:
        os.remove(link_name)

    if created_file:
        os.remove(path)


def test_os_link(os_link_fixture):
    source, link_name, expected_exception = os_link_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.link(source, link_name)
    else:
        os.link(source, link_name)


def test_os_symlink(os_link_fixture):
    source, link_name, expected_exception = os_link_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.symlink(source, link_name)
    else:
        os.symlink(source, link_name)


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-directory"), 0755, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-directory"), 0755, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-directory"), 0755,
     shield.common.ShieldError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-directory"), None, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-directory"), 0755,
     shield.common.ShieldError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-directory"), "x", TypeError),
])
def os_mkdir_fixture(request):
    path, mode, expected_exception = request.param

    shield.install_hooks()
    try:
        yield (path, mode, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if expected_exception is None:
        os.rmdir(path)


def test_os_mkdir(os_mkdir_fixture):
    path, mode, expected_exception = os_mkdir_fixture

    if mode is None:
        def call():
            os.mkdir(path)
    else:
        def call():
            os.mkdir(path, mode)

    if expected_exception:
        with pytest.raises(expected_exception):
            call()
    else:
        call()


def test_os_makedirs(os_mkdir_fixture):
    path, mode, expected_exception = os_mkdir_fixture

    if mode is None:
        def call():
            os.makedirs(path)
    else:
        def call():
            os.makedirs(path, mode)

    if expected_exception:
        with pytest.raises(expected_exception):
            call()
    else:
        call()


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True,
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"),
     False, OSError),
    (0, False, TypeError),
])
def os_remove_fixture(request):
    created_file = False
    path, should_create, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (path, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file and expected_exception is not None:
        os.remove(path)


def test_os_remove(os_remove_fixture):
    path, expected_exception = os_remove_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.remove(path)
    else:
        os.remove(path)


def test_os_unlink(os_remove_fixture):
    path, expected_exception = os_remove_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.unlink(path)
    else:
        os.unlink(path)


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-directory"), True, None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-directory"), True, None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-directory"), True,
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-directory"),
     False, OSError),
    (0, False, TypeError),
])
def os_rmdir_fixture(request):
    created_directory = False
    path, should_create, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        os.mkdir(path)
        created_directory = True

    shield.install_hooks()
    try:
        yield (path, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_directory and expected_exception is not None:
        os.rmdir(path)


def test_os_rmdir(os_rmdir_fixture):
    path, expected_exception = os_rmdir_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.rmdir(path)
    else:
        os.rmdir(path)


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"), True,
     os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file"),
     None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file"), True,
     os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"),
     None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file"), True,
     os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"),
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"), True,
     os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file"),
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"), False,
     os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file"),
     shield.common.ShieldError),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file"), False,
     os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file"),
     OSError),
    (0, False, 0, TypeError),
])
def os_rename_fixture(request):
    created_file = False
    src, should_create, dst, expected_exception = request.param

    if should_create:
        src = shield.common.make_unique(src)
        with open(src, 'w') as f:
            f.write("test\n")
        created_file = True

    shield.install_hooks()
    try:
        yield (src, dst, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file:
        if expected_exception is None:
            os.remove(dst)
        else:
            os.remove(src)


def test_os_rename(os_rename_fixture):
    src, dst, expected_exception = os_rename_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.rename(src, dst)
    else:
        os.rename(src, dst)
