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
version. See the file LICENSE.md for a copy of this license.
"""

import datetime
import math
import random
import sys

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.
from chapter_scripts.generic_chapter import write_generic_story


# First, set up constants
debugging = False

chain_length = 2
chapter_length = 9                              # Measured in sentences.
sentences_per_paragraph = 6                     # On average, in this chapter. Note this doesn't model the Joyce chapter in this regard.
mixin_texts_dir = ds.current_run_corpus_directory / '18'


def end_prob(length):
    """Calculate the probability of ending given the current story length"""
    return 1 - math.e ** (length * -3.5e-07)


def write_story():
    the_text = ''
    while random.random() >= end_prob(len(the_text)):
        the_text += " " + write_generic_story(chain_length, chapter_length, sentences_per_paragraph,
                                              ds.penelope_base_text_path, mixin_texts_dir)
    the_text += f"\n\nTrieste-Zurich-Paris 1914—1921\n"\
                f"Santa Barbara-Denver-St. Paul-Los Angeles 2015—{datetime.datetime.now().year}"
    return the_text


if __name__ == "__main__":
    print(write_story())
