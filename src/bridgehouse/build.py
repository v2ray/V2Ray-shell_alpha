#!/usr/bin/env python3

from pathlib import Path
import shutil, os, sys

if (Path("bridge.py").exists() and Path("v2ray-shell.spec").exists() and sys.platform.startswith('win')):
    """
    DEVELOPER USE ONLY, NO ANY SUPPORT OR BUG REPORT!!
    """
    file = "v2ray-shell.exe"
    os.system('"{} {}"'.format("pyinstaller", "v2ray-shell.spec"))
    if (Path(file).exists()):os.remove(file)
    try:
        shutil.rmtree("./build")
        shutil.move("./dist/" + file, "./")
        shutil.rmtree("./dist")
        shutil.rmtree("./__pycache__")
    except Exception: pass