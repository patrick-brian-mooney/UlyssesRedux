#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to create the text generated based on the eighteenth chapter of
Joyce's Ulysses, 'Penelope.' Currently, just generates 9 sentences based on
the text of 'Penelope', aiming for an average paragraph length of 1.222, which
is the actual number of sentences and average paragraph length from that
chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import datetime, sys

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.
from chapter_scripts.generic_chapter import write_generic_story


# First, set up constants
chain_length = 2
chapter_length = 9                            # Measured in sentences.
sentences_per_paragraph = 1.2222222222        # On average, in this chapter
mixin_texts_dir = '%s18' % current_run_corpus_directory

def write_story():
    return write_generic_story(chain_length, chapter_length, sentences_per_paragraph, penelope_base_text_path, mixin_texts_dir) +"""

Trieste-Zurich-Paris 1914-1921\nSanta Barbara 2015–%s""" % datetime.datetime.now().year


if __name__ == "__main__":
    debugging = True
    print(write_story())
