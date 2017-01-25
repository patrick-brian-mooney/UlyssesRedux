#!/usr/bin/env python3
"""Script called by many other chapter scripts to do the legwork of writing
a generic chapter of Ulysses Redux. Pass in a lot of parameters, get back
a chapter!

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

debugging = False

import sys, glob, os

if debugging: import pprint

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *

def buildMapping_withMixins(chain_length,               # In words
                            joyce_text_list,            # Path to file representing Joyce's text under consideration
                            mixin_texts_list,           # Loc of mixin texts
                            joyce_ratio=1.2):           # How much Joyce relative to mixins?
    if debugging: print("buildMapping_withMixins() called; parameters are ...\n\n" + pprint.pformat(locals()))
 
    joyce_text_length = mixin_texts_length = 0
    for which_file in joyce_text_list:
        joyce_text_length += os.stat(which_file).st_size
    for which_file in mixin_texts_list:
        mixin_texts_length += os.stat(which_file).st_size

    joyce_word_list = [][:]
    for the_file in joyce_text_list:
        joyce_word_list += word_list(the_file)
    joyce_scale_factor = max(int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio )), 1)   # This ratio must be at least 1, or the Joyce drops out!
    joyce_word_list *= joyce_scale_factor
    
    the_word_list = joyce_word_list.copy()
    for the_file in mixin_texts_list:
        the_word_list += word_list(the_file)

    if debugging:
        print('file lengths calculated...')
        print('  joyce_text_length is: %d' % joyce_text_length)
        print('  mixin_texts_length is: %d' % mixin_texts_length)
        print('  joyce_scale_factor is: %d' % joyce_scale_factor)
        print("  length of joyce_word_list is %d; that's %d unique words" % (len(joyce_word_list), len(set(joyce_word_list))))
        print("  length of the_word_list is %d; that's %d unique words" % (len(the_word_list), len(set(the_word_list))))
        print("  %d words in the_word_list are non-Joycean" % len(set(the_word_list).difference(set(joyce_word_list))) )
        print('\n\n    Building mappings ...')
    return buildMapping(the_word_list, markov_length=chain_length)


def write_generic_story(chain_length,
                        chapter_length,             # In sentences
                        sentences_per_paragraph,    # On average
                        joyce_text_path,
                        mixin_texts_dir,
                        joyce_ratio=1.2):
    starts, the_mapping = buildMapping_withMixins(chain_length, [joyce_text_path], glob.glob('%s/*txt' % mixin_texts_dir), joyce_ratio)
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=chapter_length,
               paragraph_break_probability=(1/sentences_per_paragraph))


if __name__ == "__main__":
    import random
    debugging = True
    print('RUNNING SELF-TEST CODE ... Writing random Joyce-Lovecraft mashup.')
    print(write_generic_story(random.choice(range(2,4)), random.choice(range(20,80)), random.choice(range(4,8)),
        random.choice(glob.glob('%s/%s/%s/*txt' % (base_directory, corpora_directory, ulysses_corpus_directory))),
        '/lovecraft/corpora/previous/', joyce_ratio=0.6))
