#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in a chapter. Makes a lot of assumptions about the structure of the text file,
including one paragraph per line with no blank lines.

usage: get_chapter_stats FILE, where FILE is the chapter filename.
"""
import sys, os, re
import nltk

sections_path = '/UlyssesRedux/corpora/joyce/ulysses/10/'
stats_file_name = '/UlyssesRedux/stats/10-stats.csv'
chapter_sections = 19

stats_file = open(stats_file_name, 'w')
stats_file.write("section number,number of paragraphs,number of sentences,number of words\n")

# OK: for each section in the chapter, produce a line indicating basic stats for that section
for which_section in range(1, 1 + chapter_sections):
    section_file = open(sections_path + '%02d.txt' % which_section)
    section_text = section_file.read()
    num_paragraphs = len(section_text.split('\n'))
    num_sentences = len(re.findall(r"[\w]+[.!?]", section_text))
    num_words = len(re.findall(r"[\w']+|[.,!?;—․]", section_text))
    section_file.close()
    stats_file.write('%d,%d,%d,%d\n' % (which_section,num_paragraphs, num_sentences, num_words))

stats_file.close()