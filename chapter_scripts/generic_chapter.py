#!/usr/bin/env python3
"""Script called by many other chapter scripts to do the legwork of writing
a generic chapter of Ulysses Redux. Pass in a lot of parameters, get back
a chapter!

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

debugging = False

import sys, glob, os, pprint

if debugging: import pprint

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
import text_generator as tg

def train_with_mixins(genny,                         # An object of type tg.TextGenerator(), which this procudure will train
                      chain_length,                  # In words
                      joyce_text_list,               # List of files representing Joyce's text under consideration
                      mixin_texts_list,              # List of mixin texts
                      joyce_ratio=1.2):              # How much Joyce relative to mixin textss?
    if debugging: print("train_withMixins() called; parameters are ...\n\n" + pprint.pformat(locals()))
 
    joyce_text_length, mixin_texts_length = 0, 0
    for which_file in joyce_text_list:
        joyce_text_length += os.stat(which_file).st_size
    for which_file in mixin_texts_list:
        mixin_texts_length += os.stat(which_file).st_size

    # This ratio must be at least 1, or the Joyce drops out!
    joyce_scale_factor = max(int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio )), 1)    
    text_list = joyce_text_list * joyce_scale_factor + mixin_texts_list

    if debugging:
        print('file lengths calculated...')
        print('  joyce_text_length is: %d' % joyce_text_length)
        print('  mixin_texts_length is: %d' % mixin_texts_length)
        print('  joyce_scale_factor is: %d' % joyce_scale_factor)
        print('\n\n    Training generator ...')
    
    genny.train(the_files=text_list, markov_length=chain_length)


def write_generic_story(chain_length,
                        chapter_length,             # In sentences
                        sentences_per_paragraph,    # On average
                        joyce_text_path,            # A list
                        mixin_texts_dir,            # Full path
                        joyce_ratio=1.2):
    genny = tg.TextGenerator()
    train_with_mixins(genny, chain_length, [joyce_text_path], glob.glob('%s/*txt' % mixin_texts_dir), joyce_ratio)
    return genny.gen_text(sentences_desired=chapter_length, paragraph_break_probability=(1/sentences_per_paragraph))


if __name__ == "__main__":
    import random
    debugging = True
    print('RUNNING SELF-TEST CODE ... Writing random Joyce-Lovecraft mashup.')
    print(write_generic_story(random.choice(range(2,4)), random.choice(range(20,80)), random.choice(range(4,8)),
        random.choice(glob.glob('%s/%s/%s/*txt' % (base_directory, corpora_directory, ulysses_corpus_directory))),
        '/lovecraft/corpora/previous/', joyce_ratio=0.6))
