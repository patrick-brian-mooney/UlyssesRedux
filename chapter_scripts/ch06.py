#!/usr/bin/env python3
"""Script to create the text generated based on the sixth chapter of Joyce's
Ulysses, 'Hades.' Currently, just generates 408 sentences based on the
text of 'Hades', aiming for an average paragraph length of 4.63, which
is the actual number of sentences and average paragraph length from that
chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.
"""

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

# First, set up constants
chain_length = 2
chapter_length = 1871                         # Measured in sentences.
sentences_per_paragraph = 4.6311881188        # On average, in this chapter

sys.path.append(markov_generator_path)
from sentence_generator import *

def write_story():
    starts, the_mapping = buildMapping(word_list(hades_base_text_path), markov_length=chain_length)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
              paragraph_break_probability=(1/sentences_per_paragraph))

if __name__ == "__main__":
    debugging = True
    print(write_story())
