import os
import shutil
import subprocess
import sys


def open_path(path):

    if sys.platform == "win32":
        os.startfile(path)

    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])

    else:
        subprocess.Popen(["xdg-open", path])


def create_file(path):

    with open(path, "w", encoding="utf-8"):
        pass


def copy_file(source, destination):

    shutil.copy2(
        source,
        destination,
    )

def rename_file(source, destination):
    os.rename(source, destination)

def delete_file(path):

    os.remove(path)