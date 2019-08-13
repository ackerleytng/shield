import os
import stat
import zipfile
import shutil
import traceback
import pytest
import shield


test_file_contents = "test\n"


def build_zip_file(path):
    with zipfile.ZipFile(path, mode='w') as f:
        f.writestr("test.txt", test_file_contents)

@pytest.fixture(params=[
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.zip"),
     os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-directory"),
     True, None),
    """
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, os.O_RDWR,
     shield.common.ShieldError),
    (os.path.join(os.path.expanduser("~"),
                  "unique-nonexistent-file.txt"), True, None, TypeError),
    (os.path.join(shield.common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, "x", TypeError),
    """
])
def os_open_fixture(request):
    created_dir = False
    src, dst, should_create, expected_exception = request.param

    build_zip_file(src)

    if should_create:
        dst = shield.common.make_unique(dst)
        os.mkdir(dst)
        created_dir = True

    shield.install_hooks()
    try:
        yield (path, flags, expected_exception)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if created_dir:
        shutil.rmtree(dst)


def test_os_open(os_open_fixture):
    test_string = "coffee\n"
    path, flags, expected_exception = os_open_fixture
    if expected_exception:
        with pytest.raises(expected_exception):
            fd = os.open(path, flags)
    else:
        fd = os.open(path, flags)
        if flags == os.O_RDONLY:
            assert os.read(fd, len(test_file_contents)) == test_file_contents
        else:
            os.write(fd, test_string)
        os.close(fd)

        if flags == os.O_RDONLY:
            assert os.stat(path).st_size == len(test_file_contents)
        elif flags & os.O_TRUNC:
            assert os.stat(path).st_size == len(test_string)
        else:
            assert os.stat(path).st_size == (len(test_string) +
                                             len(test_file_contents))
