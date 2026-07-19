#!/usr/bin/env python3
"""Script called by many other chapter scripts to do the legwork of writing
a generic chapter of Ulysses Redux. Pass in a lot of parameters, get back
a chapter!

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""


import numbers
import os
import pprint
import sys

from pathlib import Path
from typing import List


sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds    # Gets us the listing of file and directory locations.

sys.path.append(ds.markov_generator_path)
import text_generator as tg


debugging = True


def train_with_mixins(genny: tg.TextGenerator,
                      chain_length: int,
                      joyce_text_list: List[Path],
                      mixin_texts_list: List[Path],
                      joyce_ratio: numbers.Real = 1.1) -> None:
    """Train GENNY, a TextGenerator, according to the specified parameters.

    Modifies GENNY in place and returns None.
    """
    assert isinstance(joyce_text_list, list)
    assert all([isinstance(f, Path) for f in joyce_text_list])
    assert isinstance(mixin_texts_list, list)
    assert all([isinstance(f, Path) for f in mixin_texts_list])

    if debugging:
        print("train_withMixins() called; parameters are ...\n\n" + pprint.pformat(locals()))

    joyce_text_length, mixin_texts_length = 0, 0
    for which_file in joyce_text_list:
        joyce_text_length += os.stat(which_file).st_size
    for which_file in mixin_texts_list:
        mixin_texts_length += os.stat(which_file).st_size

    # This ratio must be at least 1.0, or the Joyce drops out!
    joyce_scale_factor = max(int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio )), 1.0)
    text_list = joyce_text_list * joyce_scale_factor + mixin_texts_list

    if debugging:
        print('file lengths calculated...')
        print(f'  joyce_text_length is: {joyce_text_length}')
        print(f'  mixin_texts_length is: {mixin_texts_length}')
        print(f'  joyce_scale_factor is: {joyce_scale_factor}')
        print('\n\n    Training generator ...')

    genny.train(the_files=text_list, markov_length=chain_length)


def write_generic_story(chain_length: int,
                        chapter_length: int,
                        sentences_per_paragraph: numbers.Real,
                        joyce_text_dir: Path,
                        mixin_texts_dir: Path,
                        joyce_ratio: float = 1.2) -> str:
    """Produce and return a "story" by training a TextGenerator appropriately and using
    it to produce text.

    CHAIN_LENGTH is the length (in words) of the Markov chains to use.
    CHAPTER_LENGTH is the length (in sentences) of the story to be generated.
    SENTENCES_PER_PARAGRAPH is the average number of sentences desired in a
      paragraph. (The text generator will try to approximate this but no particular
      accuracy can be promised.)
    JOYCE_TEXTS_DIR is a Path to the directory where the chapters of Ulysses are
      stored.
    MIXIN_TEXTS_DIR is a Path to the directory where the mix-in texts are stored.
    JOYCE_RATIO is the (approximate) ratio of Ulysses text to mix-in text used to
      train the generator.
    """
    assert isinstance(joyce_text_dir, Path)
    assert isinstance(mixin_texts_dir, Path)

    genny = tg.TextGenerator()
    train_with_mixins(genny=genny,
                      chain_length=chain_length,
                      joyce_text_list=[joyce_text_dir],
                      mixin_texts_list=list(mixin_texts_dir.glob('*txt')),
                      joyce_ratio=joyce_ratio)
    return genny.gen_text(sentences_desired=chapter_length,
                          paragraph_break_probability=(1/sentences_per_paragraph))


if __name__ == "__main__":
    import random
    debugging = True
    print('RUNNING SELF-TEST CODE ... Writing random Joyce-Lovecraft mashup.')
    print(write_generic_story(chain_length=random.choice(range(2, 5)),
                              chapter_length=random.choice(range(20, 80)),
                              sentences_per_paragraph=random.choice(range(4, 8)),
                              joyce_text_dir=Path(random.choice(ds.ulysses_corpus_directory.glob('%s/*txt'))),
                              mixin_texts_dir=Path('/lovecraft/corpora/previous/'),
                              joyce_ratio=0.6))
