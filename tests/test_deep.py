import os
import sys
import pytest
import shutil
import shield


@pytest.mark.parametrize("base_path, expected_exception", [
    (shield.common.get_temp_path(), None),
    (os.path.expanduser("~"), shield.common.ShieldError),
])
def test_shutil_rmtree(base_path, expected_exception):
    path = os.path.join(base_path, "unique-nonexistent-directory")
    os.mkdir(path)
    
    file_path = os.path.join(path, "unique-nonexistent-file.txt")
    with open(file_path, 'w') as f:
        f.write("test\n")

    shield.install_hooks()
    try:
        if expected_exception:
            with pytest.raises(expected_exception):
                shutil.rmtree(path)
        else:
            shutil.rmtree(path)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if expected_exception:
        shutil.rmtree(path)


@pytest.mark.parametrize("src_path, dst_path, expected_exception", [
    (shield.common.get_temp_path(), shield.common.get_desktop_path(), 
     None),
    (os.path.expanduser("~"), shield.common.get_temp_path(), 
     shield.common.ShieldError),
    (shield.common.get_temp_path(), os.path.expanduser("~"), 
     shield.common.ShieldError),
    (os.path.expanduser("~"), os.path.dirname(sys.executable),
     shield.common.ShieldError),
])
def test_shutil_move(src_path, dst_path, expected_exception):
    src_path = os.path.join(src_path, "unique-nonexistent-directory")
    os.mkdir(src_path)
    
    file_path = os.path.join(src_path, "unique-nonexistent-file.txt")
    with open(file_path, 'w') as f:
        f.write("test\n")

    shield.install_hooks()
    try:
        if expected_exception:
            with pytest.raises(expected_exception):
                shutil.move(src_path, dst_path)
        else:
            shutil.move(src_path, dst_path)
    except Exception:
        traceback.print_exc()
    finally:
        shield.uninstall_hooks()

    if expected_exception:
        shutil.rmtree(src_path)
    else:
        final_path = os.path.join(dst_path, "unique-nonexistent-directory")
        shutil.rmtree(final_path)
