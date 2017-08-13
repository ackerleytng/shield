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
                                            ["Users", "john", "Desktop",
                                             "foo", "bar.txt"])),
])
def test_split_path_windows(in_, expected):
    assert common.split_path(in_) == expected
