#!/usr/bin/env python3
"""Script to create the text generated based on the thirteenth chapter of
Joyce's Ulysses, 'Nausicaa.' Currently, just generates 1424 sentences based on
the text of 'Nausicaa', aiming for an average paragraph length of 10.17, which
is the actual number of sentences and average paragraph length from that
chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""
import sys

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.
from chapter_scripts.generic_chapter import write_generic_story


# First, set up constants
chain_length = 2
chapter_length = 1424                         # Measured in sentences.
sentences_per_paragraph = 10.1714285714       # On average, in this chapter
mixin_texts_dir = '%s13' % current_run_corpus_directory

def write_story():
    return write_generic_story(chain_length, chapter_length, sentences_per_paragraph, nausicaa_base_text_path, mixin_texts_dir)

if __name__ == "__main__":
    debugging = True
    print(write_story())
