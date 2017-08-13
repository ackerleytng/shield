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
    ("//hostname/shared drive/bar.txt", ("//hostname/shared drive", ["/", "bar.txt"])),
    (r"\\hostname\shared drive", (r"\\hostname\shared drive", [])),
    ("\\foo", ("", ["\\", "foo"])),
    # Windows sees this as empty paths after foo
    ("foo\\", ("", ["foo"])),
])
def test_split_path_windows(in_, expected):
    assert common.split_path(in_) == expected


@pytest.mark.skipif(common.running_on_windows(),
                    reason="Skipping Windows-only tests")
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
    # *nixes see this as an uncommon filename
    ("foo\\", ("", ["foo\\"])),
])
def test_split_path_non_windows(in_, expected):
    assert common.split_path(in_) == expected
