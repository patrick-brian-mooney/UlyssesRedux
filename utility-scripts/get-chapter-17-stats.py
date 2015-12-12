#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in this particular chapter, encoding basic facts about structure that are
relevant to the script 17.py. Makes a lot of assumptions about the structure of
the text file it's processing, including the assumption of one paragraph per
line with no blank lines.

usage: ./get_chapter_17_stats.py.
"""
import sys, os, re

filename = '/UlyssesRedux/corpora/joyce/ulysses/17.txt'
stats_file_name = os.path.splitext(filename)[0] + '-stats.csv'

ch7_text = open(filename).readlines()
the_stats_file = open('%s-stats.csv' % filename, 'w')

for the_line in [ which_line for which_line in ch7_text if len(which_line.strip()) > 0 ]:
    num_sents = len(list(filter(None, re.split("[!?.]+", the_line))))
    num_tokens = len(the_line.split(' '))
    if the_line[0:4] == "    ":                 # It's a question, even if it doesn't end with a question mark.
        the_stats_file.write('?')     # indicate a header by beginning with H
    else:
        the_stats_file.write(' ')     # or just begin with a space for answer text.
    the_stats_file.write('%d,%d\n' % (num_sents, num_tokens))      # Line format: # of sentences +  + newline

the_stats_file.close()