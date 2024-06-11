import os
import shutil

def copy_dir(path_source, path_dest):
    if not os.path.exists(path_source):
        raise Exception(f"{path_source} doesn't exist")
    if not os.path.isdir(path_source):
        raise Exception(f"{path_source} is not a directory")

    if not os.path.exists(path_dest):
        os.mkdir(path_dest)

    for item in os.listdir(path_source):
        __copy_dir_helper(path_source, path_dest, item)
        
def __copy_dir_helper(content_dir, dest_dir, content):
    content_source = os.path.join(content_dir, content)
    content_dest = os.path.join(dest_dir, content)

    if os.path.isfile(content_source):
        shutil.copy(content_source, content_dest)
    else:
        if not os.path.exists(content_dest):
            os.mkdir(content_dest)
        for item in os.listdir(content_source):
            __copy_dir_helper(content_source, content_dest, item)