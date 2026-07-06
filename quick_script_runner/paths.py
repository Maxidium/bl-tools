import os

from .config import CATEGORY_FOLDERS


def addon_dir():
    return os.path.dirname(__file__)

def scripts_root():
    return os.path.join(addon_dir(), "scripts")


def category_dir(category):
    folder = CATEGORY_FOLDERS.get(category, "misc")

    path = os.path.join(scripts_root(), folder)

    os.makedirs(path, exist_ok=True)

    return path