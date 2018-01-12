#!/usr/bin/env python3

from pathlib import Path
import shutil, os, sys
from PyInstaller.__main__ import run

is_win = sys.platform.startswith('win')
spec = "v2ray-shell.spec"

if (Path("bridge.py").exists() and Path(spec).exists()):
    """
    DEVELOPER USE ONLY, NO ANY SUPPORT OR BUG REPORT!!
    """
    file = "v2ray-shell"
    if is_win:
        file = "v2ray-shell.exe"

    if len(sys.argv) == 1:
        sys.argv.append(spec)
    run()

    if (Path(file).exists()):os.remove(file)
    try:
        shutil.rmtree("./build")
        shutil.move("./dist/" + file, "./")
        shutil.rmtree("./dist")
        shutil.rmtree("./__pycache__")
    except Exception: pass
