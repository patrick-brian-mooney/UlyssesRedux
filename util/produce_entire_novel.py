#!/usr/bin/env python3
"""Produces 18 chapters at once. Then it runs the postprocessing script, which (in
turn) offers the chance to set up the next run.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import sys

import pyximport; pyximport.install()           # https://cython.org/


sys.path.append('/UlyssesRedux/scripts/')
import daily_script as ds
import util.postprocess_set as ps


for which_chapter in range(0, 18):
    ds.do_write_chapter()

ps.do_postprocess()
