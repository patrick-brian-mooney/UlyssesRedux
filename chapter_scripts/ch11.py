#!/usr/bin/env python3
"""Script to create the text generated based on the eleventh chapter of Joyce's
Ulysses, 'Sirens.' Currently, just generates 642 sentences based on the text of
'Sirens', aiming for an average paragraph length of 4.04, which is the actual
number of sentences and average paragraph length from that chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.
"""

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *

# First, set up constants
chain_length = 2
chapter_length = 2597                         # Measured in sentences.
sentences_per_paragraph = 4.0451713396        # On average, in this chapter

def write_story():
    starts, the_mapping = buildMapping(word_list(sirens_base_text_path), markov_length=chain_length)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
               paragraph_break_probability=(1/sentences_per_paragraph))

if __name__ == "__main__":
    debugging = True
    print(write_story())
