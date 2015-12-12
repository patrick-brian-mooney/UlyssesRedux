#!/usr/bin/env python3
"""Script to create the text generated based on the eleventh chapter of Joyce's
Ulysses, 'Sirens.' Currently, just generates 642 sentences based on the text of
'Sirens', aiming for an average paragraph length of 4.04, which is the actual
number of sentences and average paragraph length from that chapter.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.
"""

# First, set up constants
markov_generator_path = '/UlyssesRedux/code/markov-sentence-generator'
joyce_base_text_path = '/UlyssesRedux/corpora/joyce/ulysses/11.txt'
chain_length = 3
chapter_length = 642                          # Measured in sentences.
sentences_per_paragraph = 4.0451713396        # On average, in this chapter

import sys
sys.path.append(markov_generator_path)
from sentence_generator import *

starts, the_mapping = buildMapping(word_list(joyce_base_text_path), markov_length=chain_length)
print(gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length, paragraph_break_probability=(1/sentences_per_paragraph)))
