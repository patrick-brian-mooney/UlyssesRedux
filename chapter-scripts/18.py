#!/usr/bin/env python3
"""Script to create the text generated based on the eighteenth chapter of
Joyce's Ulysses, 'Penelope.' Currently, just generates 9 sentences based on
the text of 'Penelope', aiming for an average paragraph length of 1.222, which
is the actual number of sentences and average paragraph length from that
chapter.

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
chapter_length = 9                            # Measured in sentences.
sentences_per_paragraph = 1.2222222222        # On average, in this chapter

starts, the_mapping = buildMapping(word_list(penelope_base_text_path), markov_length=chain_length)
print(gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length, paragraph_break_probability=(1/sentences_per_paragraph)) + "\n\nTrieste-Zurich-Paris 1914-1921\nSanta Barbara 2015")