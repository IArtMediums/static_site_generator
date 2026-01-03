import os
import shutil


def prepare_directories():
    static_dir = "static"
    public_dir = "docs"
    if not os.path.exists(static_dir):
        print("static directory is missing")
        return
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    copy_static_to_public(static_dir)


def copy_static_to_public(current_dir, current_public_dir=None):
    if not current_public_dir:
        current_public_dir = "docs"
        os.mkdir(current_public_dir)
    files_to_copy = os.listdir(current_dir)
    if len(files_to_copy) == 0:
        return
    for file in files_to_copy:
        static_file_path = os.path.join(current_dir, file)
        if os.path.isfile(static_file_path):
            shutil.copy(static_file_path, current_public_dir)
            continue
        next_public_dir = os.path.join(current_public_dir, file)
        os.mkdir(next_public_dir)
        copy_static_to_public(static_file_path, next_public_dir)


prepare_directories()
