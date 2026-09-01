#!/usr/bin/env python3
"""Script called by many other chapter scripts to do the legwork of writing
a generic chapter of Ulysses Redux. Pass in a lot of parameters, get back
a chapter!

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import glob
import numbers
import os
import pprint
import sys

from pathlib import Path
from typing import List

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.

sys.path.append(ds.markov_generator_path)
import text_generator as tg


debugging = False


def train_with_mixins(genny: tg.TextGenerator,
                      chain_length: int,
                      joyce_text_list: List[Path],
                      mixin_texts_list: List[Path],
                      joyce_ratio: float = 1.1,) -> None:
    """Trains GENNY, a tg.TextGenerator (or subclass, I suppose) on the provided
    texts, at the given parameters. Modifies GENNY in place and returns None.
    """
    assert isinstance(joyce_text_list, list)
    assert isinstance(mixin_texts_list, list)
    assert all([isinstance(f, Path) for f in joyce_text_list])
    assert all([isinstance(f, Path) for f in mixin_texts_list])
    if debugging:
        print("train_withMixins() called; parameters are ...\n\n" + pprint.pformat(locals()))

    joyce_text_length, mixin_texts_length = 0, 0
    for which_file in joyce_text_list:
        joyce_text_length += os.stat(which_file).st_size
    for which_file in mixin_texts_list:
        mixin_texts_length += os.stat(which_file).st_size

    # This ratio must be at least 1, or the Joyce drops out!
    joyce_scale_factor = max(int(round((mixin_texts_length / joyce_text_length) * joyce_ratio )), 1)

    if debugging:
        print('file lengths calculated...')
        print(f'  joyce_text_length is: {joyce_text_length}')
        print(f'  mixin_texts_length is: {mixin_texts_length}')
        print(f'  joyce_scale_factor is: {joyce_scale_factor}')
        print('\n\n    Training generator ...')

    for which_t in joyce_text_list:
        genny.train_from_text(the_text=which_t.read_text(encoding='utf-8'), markov_length=chain_length,
                              weight=joyce_ratio, learn_starts=True)
    for which_t in mixin_texts_list:
        genny.train_from_text(the_text=which_t.read_text(encoding='utf-8'), markov_length=chain_length)
    genny.finalize_mapping()


def write_generic_story(chain_length: int,
                        chapter_length: int,
                        sentences_per_paragraph: numbers.Real,
                        joyce_text_path: Path,
                        mixin_texts_dir: Path,            # Full path
                        joyce_ratio: float = 1.2) -> str:
    """Train a tg.TextGenerator on the provided texts, given the specified parameters,
    and use it to produce and return a "story."
    """
    genny = tg.TextGenerator()
    train_with_mixins(genny, chain_length, [joyce_text_path],
                      list(mixin_texts_dir.glob('*txt')), joyce_ratio)
    return genny.gen_text(sentences_desired=chapter_length, paragraph_break_probability=(1/sentences_per_paragraph))


if __name__ == "__main__":
    import random
    debugging = True
    print('RUNNING SELF-TEST CODE ... Writing random Joyce-Lovecraft mashup.')
    print(write_generic_story(random.choice(range(2,4)), random.choice(range(20,80)), random.choice(range(4,8)),
        random.choice(list(ds.ulysses_corpus_directory.glob('*txt'))),
        '/lovecraft/corpora/previous/', joyce_ratio=0.6))
