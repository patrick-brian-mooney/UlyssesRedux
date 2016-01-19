#!/usr/bin/env python3
"""Script to create the text generated based on the fourth chapter of Joyce's
Ulysses, 'Calypso.' Currently, just generates 108 sentences based on the text
of 'Calypso', aiming for an average paragraph length of 6.787, which is the
actual number of sentences and average paragraph length from that chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.
"""

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

# First, set up constants
chain_length = 2
chapter_length = 953                          # Measured in sentences.
sentences_per_paragraph = 5.2944444444        # On average, in this chapter

sys.path.append(markov_generator_path)
from sentence_generator import *

def write_story():
    starts, the_mapping = buildMapping(word_list(calypso_base_text_path), markov_length=chain_length)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
               paragraph_break_probability=(1/sentences_per_paragraph))

if __name__ == "__main__":
    debugging = True
    print(write_story())
