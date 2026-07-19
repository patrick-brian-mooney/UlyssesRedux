#!/usr/bin/env python3
"""Script to create the text generated based on the first chapter of Joyce's
Ulysses, 'Telemachus.' Currently, just generates 366 sentences based on the
text of 'Telemachus, aiming for an average paragraph length of 3.7, which
is the actual number of sentences and average paragraph length from that chapter

A Markov length of 2 seems to work well here, according to insufficient tests
evaluated informally.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds    # Gets us the listing of file and directory locations.
from chapter_scripts.generic_chapter import write_generic_story


# First, set up constants
CHAIN_LENGTH = 2
CHAPTER_LENGTH = 986                    # Measured in sentences.
SENTENCES_PER_PARAGRAPH = 2.693989071   # On average, in this chapter
MIXIN_TEXTS_DIR = ds.current_run_corpus_directory / '01'


def write_story() -> str:
    return write_generic_story(CHAIN_LENGTH, CHAPTER_LENGTH, SENTENCES_PER_PARAGRAPH,
                               ds.telemachus_base_text_path, MIXIN_TEXTS_DIR)


if __name__ == "__main__":
    print(write_story())
