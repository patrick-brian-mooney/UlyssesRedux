#!/usr/bin/env python3
"""Produces 18 chapters at once. Then it runs the postprocessing script, which (in
turn) offers the chance to set up the next run.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import subprocess

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

for which_chapter in range(0, 18):
    subprocess.call([daily_script_path], shell=True)

subprocess.call([postprocessing_script], shell=True)