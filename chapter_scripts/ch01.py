#!/usr/bin/env python3
"""Script to create the text generated based on the first chapter of Joyce's
Ulysses, 'Telemachus.' Currently, just generates 366 sentences based on the
text of 'Telemachus, aiming for an average paragraph length of 3.7, which
is the actual number of sentences and average paragraph length from that chapter

A Markov length of 2 seems to work well here, according to insufficient tests
evaluated informally.
"""

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

# First, set up constants
chain_length = 2
chapter_length = 986                    # Measured in sentences.
sentences_per_paragraph = 2.693989071   # On average, in this chapter

sys.path.append(markov_generator_path)
from sentence_generator import *

def write_story():
    starts, the_mapping = buildMapping(word_list(telemachus_base_text_path), markov_length=chain_length)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
               paragraph_break_probability=(1/sentences_per_paragraph))

if __name__ == "__main__":
    debugging = True
    print(write_story())
