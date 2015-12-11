#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in this particular chapter, encoding basic facts about structure that are
relevant to the script 7.py. Makes a lot of assumptions about the structure of
the text file it's processing, including the assumption of one paragraph per
line with no blank lines.

usage: ./get_chapter_7_stats.py.
"""
import sys, os, re

filename = '/UlyssesRedux/corpora/joyce/ulysses/07.txt'
stats_file_name = os.path.splitext(filename)[0] + '-stats.csv'

ch7_text = open(filename).readlines()
the_stats_file = open('%s-stats.csv' % filename, 'w')

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