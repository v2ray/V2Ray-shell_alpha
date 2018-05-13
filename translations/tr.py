#!/usr/bin/env python3
from PyQt5 import pylupdate_main as pylupdate
import sys

profile = "../v2rayshell.pro"
sys.argv.append(profile)
pylupdate.main()