#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in a chapter. Makes a lot of assumptions about the structure of the text file,
including one paragraph per line with no blank lines.

usage: get_chapter_stats FILE, where FILE is the chapter filename.
"""
import sys, os, re

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.


chapter_sections = 19

stats_file = open(wandering_rocks_stats_file , 'w')
stats_file.write("section number,number of paragraphs,number of sentences,number of words\n")

# OK: for each section in the chapter, produce a line indicating basic stats for that section
for which_section in range(1, 1 + chapter_sections):
    section_file = open('%s/%02d.txt' % (wandering_rocks_sections_path, which_section))
    section_text = section_file.read()
    num_paragraphs = len(section_text.split('\n'))
    num_sentences = len(re.findall(r"[\w]+[.!?]", section_text))
    num_words = len(re.findall(r"[\w']+|[.,!?;—․]", section_text))
    section_file.close()
    stats_file.write('%d,%d,%d,%d\n' % (which_section,num_paragraphs, num_sentences, num_words))

stats_file.close()
