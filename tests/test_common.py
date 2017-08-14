import os
import sys
import pytest
from shield import common


@pytest.mark.parametrize("in_, expected", [
    ("", ("", [])),
    ("foo", ("", ["foo"])),
    ("foo/", ("", ["foo"])),
    ("/", ("", ["/"])),
    ("foo/bar", ("", ["foo", "bar"])),
    ("/foo/bar", ("", ["/", "foo", "bar"])),
    ("/foo/bar/", ("", ["/", "foo", "bar"])),
    ("foo/bar/", ("", ["foo", "bar"])),
    ("/tmp/foo/bar.txt", ("", ["/", "tmp", "foo", "bar.txt"])),
])
def test_split_path(in_, expected):
    assert common.split_path(in_) == expected


@pytest.mark.skipif(not common.running_on_windows(),
                    reason="Skipping Windows-only tests")
@pytest.mark.parametrize("in_, expected", [
    (r"C:\Users\john\Desktop\foo\bar.txt", ("C:",
                                            ["\\", "Users", "john", "Desktop",
                                             "foo", "bar.txt"])),
    ("c:", ("c:", [])),
    ("c:/", ("c:", ["/"])),
    ("c:/foo", ("c:", ["/", "foo"])),
    ("c:\\", ("c:", ["\\"])),
    ("c:/users/john/foo.txt", ("c:", ["/", "users", "john", "foo.txt"])),
    ("c:foo", ("c:", ["foo"])),
    # Windows sees this as a well formed path with non-windows style slashes
    #   (which it will interpret anyway)
    ("//hostname/shared drive/bar.txt", ("//hostname/shared drive",
                                         ["/", "bar.txt"])),
    (r"\\hostname\shared drive", (r"\\hostname\shared drive", [])),
    ("\\foo", ("", ["\\", "foo"])),
    # Windows sees this as empty paths after foo
    ("foo\\", ("", ["foo"])),
    # Windows sees this as a regular path since it is not long enough
    #   to be a shared drive path
    (r"\\foo", ("", [r"\\", "foo"])),
])
def test_split_path_windows(in_, expected):
    assert common.split_path(in_) == expected


@pytest.mark.skipif(common.running_on_windows(),
                    reason="Skipping non-Windows tests")
@pytest.mark.parametrize("in_, expected", [
    ("c:", ("", ["c:"])),
    ("c:/", ("", ["c:"])),
    ("c:\\", ("", ["c:\\"])),
    ("c:/foo", ("", ["c:", "foo"])),
    ("c:/users/john/foo.txt", ("", ["c:", "users", "john", "foo.txt"])),
    # *nixes see this as a single file with : in the filename
    ("c:foo", ("", ["c:foo"])),
    # *nixes see this as a file with \ in the filename
    ("\\foo", ("", ["\\foo"])),
    # *nixes see this as a file with \\ in the filename
    (r"\\foo", ("", [r"\\foo"])),
    # *nixes see this as an uncommon filename
    ("foo\\", ("", ["foo\\"])),
])
def test_split_path_non_windows(in_, expected):
    assert common.split_path(in_) == expected


@pytest.mark.parametrize("a, b, expected", [
    ([], [], True),
    ([0, 1, 2], [0, 1, 2], True),
    ([0, 1, 2, 3], [0, 1, 2], True),
    ([0, 1, 3], [0, 1, 2], False),
    ([0, 1], [0, 1, 2], False),
    (["tmp", "test"], ["tmp"], True),
])
def test_list_startswith(a, b, expected):
    assert common.list_startswith(a, b) == expected


@pytest.mark.parametrize("path, path_to_directory, expected", [
    ("/tmp/test/stuff", "/tmp/test", True),
    (r"I:\shared\stuff", r"C:\shared\stuff", False),
    (r"I:\shared\stuff", r"C:\shared\stuff\zzzz", False),
    (r"C:\shared\stuff", r"C:\shared\stuffs", False),
])
def test_is_in_directory(path, path_to_directory, expected):
    assert common.is_in_directory(path, path_to_directory) == expected


@pytest.fixture(params=[
    (common.get_desktop_path(), False, True),
    (common.get_temp_path(), False, True),
    (os.path.join(common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), True, False),
    (os.path.join(common.get_temp_path(),
                  "unique-nonexistent-file.txt"), True, False),
    (os.path.join(common.get_desktop_path(),
                  "unique-nonexistent-file.txt"), False, True),
    (os.path.join(common.get_temp_path(),
                  "unique-nonexistent-file.txt"), False, True),
    (sys.executable, False, False),
])
def is_safe_for_writing_fixture(request):
    created_file = False
    path, should_create, expected = request.param

    if should_create:
        path = common.make_unique(path)
        with open(path, 'w') as f:
            f.write("test\n")
        created_file = True

    yield (path, expected)

    if created_file:
        os.remove(path)


def test_is_safe_for_writing(is_safe_for_writing_fixture):
    path, expected = is_safe_for_writing_fixture
    assert common.is_safe_for_writing(path) == expected
