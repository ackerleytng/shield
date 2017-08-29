import io
import os
import traceback
import pytest
import shield


test_file_contents = "test\n"


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
def io_open_fixture(request):
    created_file = False
    path, should_create, mode, expected_exception = request.param

    if should_create:
        path = shield.common.make_unique(path)
        with open(path, 'w') as f:
            f.write(test_file_contents)
        created_file = True

    shield.install_hooks()
    try:
        yield (path, mode, created_file, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_file or expected_exception is None:
        os.remove(path)


def test_io_open(io_open_fixture):
    test_string = u"pineapple\n"
    path, mode, created_file, expected_exception = io_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            io.open(path, mode)
    else:
        with io.open(path, mode) as f:
            if mode == "r":
                f.read()
            else:
                f.write(test_string)

        if mode == "r":
            assert os.stat(path).st_size == len(test_file_contents)
        elif "w" in mode or mode == "r+":
            assert os.stat(path).st_size == len(test_string)
        else:
            assert os.stat(path).st_size == (len(test_string) +
                                             len(test_file_contents))


def test_io_FileIO(io_open_fixture):
    test_string = u"shampoo\n"
    path, mode, created_file, expected_exception = io_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            io.FileIO(path, mode)
    else:
        with io.FileIO(path, mode) as f:
            if mode == "r":
                f.read()
            else:
                f.write(test_string)

        if mode == "r":
            assert os.stat(path).st_size == len(test_file_contents)
        elif "w" in mode or mode == "r+":
            assert os.stat(path).st_size == len(test_string)
        else:
            assert os.stat(path).st_size == (len(test_string) +
                                             len(test_file_contents))


def test_io_open_weird():
    shield.install_hooks()
    try:
        with pytest.raises(IOError):
            # Picked 64 because 1 (used to test __builtin__)
            #   actually works for io.open()
            #   because io.open() can take fds
            io.open(64)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()
