import pytest
from shield import common


@pytest.mark.parametrize("windows_only, in_, expected", [
    (False, "foo/bar", ("", ["foo", "bar"])),
    (False, "/foo/bar", ("", ["foo", "bar"])),
    (False, "/foo/bar/", ("", ["foo", "bar"])),
    (False, "foo/bar/", ("", ["foo", "bar"])),
    (False, "/tmp/foo/bar.txt", ("", ["tmp", "foo", "bar.txt"])),
    (True, r"C:\Users\john\Desktop\foo\bar.txt", ("C:",
                                                  ["Users", "john", "Desktop",
                                                   "foo", "bar.txt"])),
])
def test_split_path(windows_only, in_, expected):
    if not common.running_on_windows() and not windows_only:
        assert common.split_path(in_) == expected
