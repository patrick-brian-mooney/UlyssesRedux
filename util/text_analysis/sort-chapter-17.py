#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sorts chapter 17 into two corpora: one with questions, one with answers. The 
sorting criterion is simply that I've preprocessed Eumaeus so that the
questions begin with four spaces, the answers don't.

usage:

    ./get_chapter_17_stats.py

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys
sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

ch17_text = open(ithaca_base_text_path).readlines()
questions_file = open(ithaca_questions_path  , 'w')
answers_file = open(ithaca_answers_path, 'w')

for the_line in [ which_line for which_line in ch17_text if len(which_line.strip()) > 0 ]:
    if the_line.startswith('    '):     # It's a questions
        questions_file.write(the_line)
    else:                               # It's an answer
        answers_file.write(the_line)
