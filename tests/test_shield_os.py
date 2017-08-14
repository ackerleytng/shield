import os
import sys
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