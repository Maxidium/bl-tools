import os

from ..paths import category_dir
from ..config import (
    ACRONYMS,
    FORMAT_SCRIPT_NAMES,
    SCRIPT_EXTENSION,
    SHOW_SCRIPT_EXTENSION,
)


def get_scripts(category):

    path = category_dir(category)

    if not os.path.isdir(path):
        return None

    scripts = []

    for file in os.listdir(path):

        if file.endswith(".py"):
            scripts.append(file)

    scripts.sort()

    return scripts


def script_label(filename):

    label = filename

    if FORMAT_SCRIPT_NAMES:

        label = label.removesuffix(SCRIPT_EXTENSION)

        words = []

        for word in label.split("_"):

            words.append(
                ACRONYMS.get(
                    word.lower(),
                    word.capitalize(),
                )
            )

        return " ".join(words)

    if not SHOW_SCRIPT_EXTENSION:
        label = label.removesuffix(SCRIPT_EXTENSION)

    return label