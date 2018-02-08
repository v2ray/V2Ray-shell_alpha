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
        import site
        file = "v2ray-shell.exe"
        packages = site.getsitepackages()
        libeay32 = packages[1]+"/PyQt5/Qt/bin/libeay32.dll"
        ssleay32 = packages[1]+"/PyQt5/Qt/bin/ssleay32.dll"
        if (Path(libeay32).exists() and Path(ssleay32).exists()):
            try:
                shutil.copy(libeay32, "./")
                shutil.copy(ssleay32, "./")
            except Exception: pass
            
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
