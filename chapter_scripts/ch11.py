#!/usr/bin/env python3
"""Script to create the text generated based on the eleventh chapter of Joyce's
Ulysses, 'Sirens.' Currently, just generates 2597 sentences based on the text of
'Sirens', aiming for an average paragraph length of 4.045, which is the actual
number of sentences and average paragraph length from that chapter.

A Markov length of 2 seems to work well here, according to insufficient tests
evaluated informally.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""

import sys

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.
from chapter_scripts.generic_chapter import write_generic_story


# First, set up constants
chain_length = 2
chapter_length = 2597                         # Measured in sentences.
sentences_per_paragraph = 4.0451713396        # On average, in this chapter
mixin_texts_dir = ds.current_run_corpus_directory / '11'


def write_story():
    return write_generic_story(chain_length, chapter_length, sentences_per_paragraph,
                               ds.sirens_base_text_path, mixin_texts_dir)


if __name__ == "__main__":
    print(write_story())
