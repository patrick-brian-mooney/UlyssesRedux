#!/usr/bin/env python3
"""Script to create the text generated based on the first chapter of Joyce's Ulysses, 'Telemachus.'
Currently, just returns the actual text of 'Telemachus' exactly as Joyce wrote it.
"""

import sys
sys.path.append('/UlyssesRedux/code/markov-sentence-generator')
from sentence_generator import *

starts, the_mapping = buildMapping(word_list('/UlyssesRedux/corpora/joyce/ulysses/01.txt'), markov_length=2)
print(gen_text(the_mapping, starts, markov_length=2, sentences_desired=24, paragraph_break_probability=0.2))