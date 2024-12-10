'''
    fileloader.py

    Used for the package, PyInstaller, 
    this file bundles all the assets and scripts
    to create a single executable file.

    Functions:
        path_of(path) -> str
'''

from pathlib import Path
import os
import sys

# Base directory for getting files, When running as a standalone PyInstaller executable
BASE_LINK = getattr(sys, "_MEIPASS", Path(os.path.abspath(os.path.dirname(__file__))).parent)

def path_of(path):
    abs_path = os.path.abspath(os.path.join(BASE_LINK, path))
    if not os.path.exists(abs_path):
        abs_path = path
    return abs_path

