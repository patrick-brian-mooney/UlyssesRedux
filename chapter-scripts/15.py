#!/usr/bin/env python3
"""Script to create the text generated based on the fifteenth chapter of
Joyce's Ulysses, 'Circe.' It runs along the structure described in the file
/UlyssesRedux/stats/15-stats.psv, which is generated by the utility script
/UlyssesRedux/code/utility-scripts/analyze-chapter-15.py, drawing from multiple
corpora and building a chapter that's based on those multiple corpora in a
similar outward form.

A Markov length of 3 seems to work well here, according to insufficient tests
evaluated informally.
"""

import glob, os
import sys

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

sys.path.append(markov_generator_path)
from sentence_generator import *

# First, set up constants
chain_length = 2
debugging_flag = False

corpora = {}.copy()

if debugging_flag: print("INFO: about to start processing corpora.")

for which_corpus in glob.glob(circe_corpora_path + '*txt'):
    if debugging_flag: print('INFO: processing "%s".' % which_corpus)
    starts, the_mapping = buildMapping(word_list(which_corpus), markov_length=chain_length)
    corpus_name = os.path.basename(which_corpus)[:-4]
    corpora[corpus_name] = [starts, the_mapping]

if debugging_flag:
    from pprint import pprint
    pprint(corpora)

the_chapter = [].copy()

def get_speaker_text(speaker_name, num_sentences):
    if speaker_name in corpora:
        which_index = speaker_name
    elif speaker_name == 'STAGE':
        which_index = 'STAGE DIRECTIONS'
    else:
        which_index = 'MINOR CHARACTERS'
    starts, the_mapping = tuple(corpora[which_index])
    return gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=num_sentences, paragraph_break_probability = 0)

if debugging_flag: print("INFO: About to process stats file.")

with open(circe_stats_path) as circe_stats_file:
    for the_encoded_paragraph in circe_stats_file:
        # Process each line, using it as a map of the corresponding paragraph in 'Circe'.
        # Structure of these lines is defined in /UlyssesRedux/code/utility-scripts/analyze-chapter-15.py.
        # But here's a quick reminder:
        # Two parts: a name of a speaker (or "STAGE" if it's a paragraph of stage directions), then a series of codes for "chunks" of the paragraph.
        # A "chunk" is a number of sentences. If the number is preceded by opening parens, it's an intraparagraph stage direction.
        # Parts of the line, and chunk descriptions, are separated by vertical bars (pipe characters), hence the .psv extension.
        if debugging_flag: print('INFO: Processing coded line "%s".' % the_encoded_paragraph)
        code_to_process = the_encoded_paragraph.split('|')
        speaker_name = code_to_process.pop(0)
        if debugging_flag: print('  speaker name is "%s".' % speaker_name)
        if speaker_name != 'STAGE':                                     # Unless the name is 'STAGE', add it to the beginning of this paragraph
            this_paragraph = '%s: ' % speaker_name
        else:                                                           # In which case, begin with an opening parenthesis.
            this_paragraph = '('
        while len(code_to_process) > 0:
            chunk_descriptor = code_to_process.pop(0)
            if debugging_flag: print('    processing chunk "%s".' % chunk_descriptor)
            if chunk_descriptor[0] == '(':
                this_paragraph = this_paragraph + '(%s) ' % (get_speaker_text('STAGE', int(chunk_descriptor[1:])))
            else:
                this_paragraph = this_paragraph + '%s ' % (get_speaker_text(speaker_name, int(chunk_descriptor)))
            if debugging_flag: print('      current paragraph length is now %d.' % len(this_paragraph))
        if speaker_name == 'STAGE':
            this_paragraph = this_paragraph.strip() + ')'
        if debugging_flag: print('        done with this paragraph; total length is %d.' % len(this_paragraph))
        the_chapter.append(this_paragraph)

print('\n'.join(the_chapter))