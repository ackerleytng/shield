import os
import shutil
import shield


def test_shutil_rmtree(base_path, expected_exception):
    shield.uninstall_hooks()
    
    path = os.path.join(base_path, "unique-nonexistent-directory")
    os.mkdir(path)
    
    file_path = os.path.join(path, "unique-nonexistent-file.txt")
    with open(file_path, 'w') as f:
        f.write("test\n")

    shield.install_hooks()

    if expected_exception:
        try:
            shutil.rmtree(path)
        except expected_exception:
            print "Correctly shielded!"
    else:
        shutil.rmtree(path)

    if expected_exception:
        shield.uninstall_hooks()
        shutil.rmtree(path)
        shield.install_hooks()

test_shutil_rmtree(shield.common.get_temp_path(), None)
test_shutil_rmtree(os.path.expanduser("~"), shield.common.ShieldError)


try:
    with open("student_script.py", 'w') as f:
        print f.read()
except shield.common.ShieldError:
    print "Correctly shielded!"


"""
os.open("/dev/null", os.O_RDONLY)

os.remove("/dummy_folder")

os.rmdir("/dummy_folder")

os.removedirs("/dummy_folder")

with io.open("test.txt", 'w') as f:
    print f.write(u"adasd")
"""
