#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in this particular chapter, encoding basic facts about structure that are
relevant to the script 7.py. Makes a lot of assumptions about the structure of
the text file it's processing, including the assumption of one paragraph per
line with no blank lines.

usage:
    ./get_chapter_7_stats.py

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""
import sys, os, re

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

ch7_text = open(aeolus_base_text_path).readlines()
the_stats_file = open(aeolus_stats_path, 'w')

for the_line in [ which_line.strip() for which_line in ch7_text if len(which_line.strip()) > 0 ]:
    num_sents = len(list(filter(None, re.split("[!?.]+", the_line))))
    num_tokens = len(the_line.split(' '))
    if the_line.strip().upper() == the_line.strip():                 # It's a headline
        the_stats_file.write('H')     # indicate a header by beginning with H
    elif the_line.startswith("--") or the_line.startswith("—"):      # It's a line of dialogue
        the_stats_file.write('—')     # indicates a quote beginning with an em dash
    else:
        the_stats_file.write(' ')     # or just begin with a space for non-headline, non-quoted text.
    the_stats_file.write('%d,%d\n' % (num_sents, num_tokens))      # Line format: # of sentences + newline

the_stats_file.close()