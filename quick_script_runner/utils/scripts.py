import os

from ..paths import category_dir


def get_scripts(category):

    path = category_dir(category)

    scripts = []

    for file in os.listdir(path):

        if file.endswith(".py"):
            scripts.append(file)

    scripts.sort()

    return scripts