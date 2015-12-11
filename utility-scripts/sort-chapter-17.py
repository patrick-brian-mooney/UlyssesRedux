#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sorts chapter 17 into two corpora: one with questions, one with answers. The 
sorting criterion is simply that I've preprocessed Eumaeus so that the
questions begin with four spaces, the answers don't.

usage: ./get_chapter_17_stats.py.
"""

ch17_filename = '/UlyssesRedux/corpora/joyce/ulysses/17.txt'
questions_filename = '/UlyssesRedux/corpora/joyce/ulysses/17/questions.txt'
answers_filename = '/UlyssesRedux/corpora/joyce/ulysses/17/answers.txt'

ch17_text = open(ch17_filename).readlines()
questions_file = open(questions_filename, 'w')
answers_file = open(answers_filename, 'w')

for the_line in [ which_line for which_line in ch17_text if len(which_line.strip()) > 0 ]:
    if the_line.startswith('    '):     # It's a questions
        questions_file.write(the_line)
    else:                               # It's an answer
        answers_file.write(the_line)
