import os
import sys
import pytest
import shield


@pytest.fixture(params=[
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, "r", None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, "r", None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, "w", None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, "w", None),
    (os.path.join(shield.common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, "a", None),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, "a", None),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, "w",
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, "a",
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, "w+",
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, "a+",
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, "r+",
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, None, TypeError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, "x", ValueError),
])
def builtin_open_fixture(request):
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


def test_builtin_open(builtin_open_fixture):
    path, mode, expected_exception = builtin_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            open(path, mode)
    else:
        open(path, mode)
