from pathlib import Path
import os
import sys

BASE_LINK = getattr(sys, "_MEIPASS", Path(os.path.abspath(os.path.dirname(__file__))).parent)

def path_of(path):
    abs_path = os.path.abspath(os.path.join(BASE_LINK, path))
    if not os.path.exists(abs_path):
        abs_path = path
    return abs_path

