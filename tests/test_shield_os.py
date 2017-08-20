import os
import sys
import stat
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
    yield (path, flags, expected_exception)
    shield.uninstall_hooks()

    if created_file:
        os.remove(path)


def test_os_open(os_open_fixture):
    path, flags, expected_exception = os_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            os.open(path, flags)
    else:
        os.open(path, flags)


@pytest.mark.parametrize("disabled_call", [
    lambda: os.chflags("/tmp/stuff", stat.SF_IMMUTABLE),
    lambda: os.chroot("/tmp/stuff"),
    lambda: os.lchflags("/tmp/stuff", stat.SF_IMMUTABLE),
])
def test_disabled(disabled_call):
    shield.install_hooks()
    with pytest.raises(shield.common.ShieldError):
        disabled_call()
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
    yield (path, mode, expected_exception)
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
    yield (path, id_, expected_exception)
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
