import os

from ..paths import category_dir
from ..config import (SCRIPT_EXTENSION,SHOW_SCRIPT_EXTENSION,)


def get_scripts(category):

    path = category_dir(category)

    scripts = []

    for file in os.listdir(path):

        if file.endswith(".py"):
            scripts.append(file)

    scripts.sort()

    return scripts

def script_label(filename):

    if SHOW_SCRIPT_EXTENSION:
        return filename

    return filename.removesuffix(SCRIPT_EXTENSION)