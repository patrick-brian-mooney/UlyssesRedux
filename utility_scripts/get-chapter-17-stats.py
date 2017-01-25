#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in this particular chapter, encoding basic facts about structure that are
relevant to the script 17.py. Makes a lot of assumptions about the structure of
the text file it's processing, including the assumption of one paragraph per
line with no blank lines.

usage:

    ./get_chapter_17_stats.py

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys, os, re
sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

stats_file_name = os.path.splitext(ithaca_base_text_path)[0] + '-stats.csv'

ch17_text = open(ithaca_base_text_path).readlines()
the_stats_file = open('%s-stats.csv' % stats_file_name, 'w')

for the_line in [ which_line for which_line in ch17_text if len(which_line.strip()) > 0 ]:
    num_sents = len(list(filter(None, re.split("[!?.]+", the_line))))
    num_tokens = len(the_line.split(' '))
    if the_line[0:4] == "    ":                 # It's an interrogative, even if it doesn't end with a question mark.
        the_stats_file.write('?')               # indicate an interrogative by beginning with ?
    else:
        the_stats_file.write(' ')               # or just begin with a space for answer text.
    the_stats_file.write('%d,%d\n' % (num_sents, num_tokens))      # Line format: # of sentences +  + newline

the_stats_file.close()
