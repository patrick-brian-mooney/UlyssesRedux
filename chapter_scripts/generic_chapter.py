#!/usr/bin/env python3
"""Script called by many other chapter scripts to do the legwork of writing
a generic chapter of Ulysses Redux. Pass in a lot of parameters, get back
a chapter!

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys, glob, os

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *

def buildMapping_withMixins(chain_length,               # In words
                            joyce_text_path,            # Path to file representing Joyce's text under consideration
                            mixin_texts_dir,            # Loc of mixin texts
                            joyce_ratio=1.4):           # How much Joyce relative to mixins?
    joyce_text_length = os.stat(joyce_text_path).st_size
    mixin_texts_length = 0
    for which_file in glob.glob('%s/*txt' % mixin_texts_dir):
        mixin_texts_length += os.stat(which_file).st_size

    the_word_list = word_list(joyce_text_path) * int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio ))
    for the_file in glob.glob('%s/*txt' % mixin_texts_dir):
        the_word_list += word_list(the_file)
    return buildMapping(the_word_list, markov_length=chain_length)


def write_generic_story(chain_length,
                        chapter_length,             # In sentences
                        sentences_per_paragraph,    # On average
                        joyce_text_path,
                        mixin_texts_dir,
                        joyce_ratio=1.4):
    starts, the_mapping = buildMapping_withMixins(chain_length, joyce_text_path, mixin_texts_dir, joyce_ratio)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
               paragraph_break_probability=(1/sentences_per_paragraph))


if __name__ == "__main__":
    import random, glob
    print('RUNNING SELF-TEST CODE ... Writing random Joyce-Lovecraft mashup.')
    print(write_generic_story(random.choice(range(2,4)), random.choice(range(20,80)), random.choice(range(4,8)),
        random.choice(glob.glob('%s/%s/%s/*txt' % (base_directory, corpora_directory, ulysses_corpus_directory))),
        '/lovecraft/corpora/previous/', joyce_ratio=0.6))
