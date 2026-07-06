import os

from .config import CATEGORIES


def addon_dir():
    return os.path.dirname(__file__)

def scripts_root():
    return os.path.join(addon_dir(), "scripts")


def category_dir(category):
    folder = next(
        folder
        for identifier, _, folder in CATEGORIES
        if identifier == category
    )

    return os.path.join(scripts_root(),folder,)

def ensure_category_dirs():

    for identifier, _, _ in CATEGORIES:

        os.makedirs(
            category_dir(identifier),
            exist_ok=True,
        )