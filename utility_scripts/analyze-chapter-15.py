#!/usr/bin/env python3
"""Produces a structure file to describe the 'Circe' chapter of Ulysses, plus
individual corpora for the script 15.py to work with.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import re

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

debugging = True

# Go over the text of 'Circe.'
# We have two goals here:
# 1. produce an appropriate dictionary, producing (a) corpora for each character, and (b) a corpus containing stage directions
# 2. Produce a structural description of Circe that can be interpreted by 15.py.

stage_directions = [].copy()
characters_lines = {}.copy()            # structure: name -> list of lines spoken by that character.

def separate_line(the_line):
    """Process a spoken line, returning a tuple: (stage directions, spoken text).
    For purposes of this function, 'stage directions' is any text in parentheses.

    This function works for paragraphs with multiple parenthetical comments (it
    returns all of the information in the parentheses, concatenated, without any
    indication of how many sets of parentheses this information came from or where
    the points are where text has been joined), but will fail on nested
    parentheses; however, these never occur in 'Circe.'
    """
    stage_directions = ""
    spoken_text = the_line
    while '(' in spoken_text:
        start_pos = spoken_text.find('(')
        end_pos = spoken_text.find(')')
        if end_pos == -1: end_pos = 100000000           # If the parens are never closed, use a really big number; clearly past the end of the paragraph.
        stage_directions = stage_directions + spoken_text[start_pos + 1:end_pos]
        stage_directions = stage_directions.strip().strip('\n').strip()
        if len(stage_directions) > 0:
            if stage_directions[-1] not in '.!?':
                stage_directons = stage_directions + '.'
            if stage_directions[-1] != ' ':
                stage_directions = stage_directions + ' '
        if len(spoken_text) > end_pos:                  # then the stage direction doesn't end the line
            spoken_text = spoken_text[0:start_pos] + ' ' + spoken_text[end_pos + 1:]
        else:
            spoken_text = spoken_text[0:start_pos]
        spoken_text = spoken_text.strip().strip('\n').strip()
        if len(spoken_text) > 0:
            if spoken_text[-1] not in '.!?':
                spoken_text = spoken_text + '.'
            if spoken_text[-1] != ' ':
                spoken_text = spoken_text + ' '
    return stage_directions.replace('  ', ' ').replace(' .', '.').strip().strip('\n').strip(), spoken_text.replace('  ', ' ').replace(' .', '.').strip().strip('\n').strip()

def num_sentences(the_text):
    return len(list(filter(None, re.split("[!?.]+", the_text))))

with open(circe_text_path) as circe_source_file, open(circe_stats_path, 'w') as circe_stats_file:
    for the_line in circe_source_file:
        if debugging: print("INFO: processing this line: " + the_line)
        split_line = the_line.split(':')
        if len(split_line) == 1 or the_line[0:4] != the_line[0:4].upper():          # It's a stage direction
            the_directions = the_line.strip('()')                                   # Strip beginning and ending parentheses.
            if len(the_directions) > 0:
                if the_directions[-1] not in '.!?':
                    the_directions = the_directions + '.'
            stage_directions.append(the_directions)                                 # Strip beginning and ending parentheses.
            structure_code = 'STAGE|'                                               # Start putting together the structure code for the line
            to_encode = the_directions
        else:                                                                       # It's a spoken line.
            character_name = split_line[0]
            structure_code = character_name + '|'               # Start putting together the structure code for the line.
            spoken_text = ':'.join(split_line[1:]).strip()      # Process the rest of the line, after the character name.
            to_encode = spoken_text
            while '(' in spoken_text:                           # Sigh. Line contains at least one stage direction.
                this_stage_direction, spoken_text = separate_line(spoken_text)
                this_stage_direction = this_stage_direction.strip()
                if len(this_stage_direction) > 0:
                    if this_stage_direction[-1] not in '.!?':
                        this_stage_direction = this_stage_direction + '.'
                stage_directions.append(this_stage_direction)
            try:
                characters_lines[character_name].append(spoken_text + "\n")
            except (KeyError, AttributeError):        # First time we've run across this character.
                characters_lines[character_name] = [].copy() + [ spoken_text + "\n" ]
        # All right, write the rest of the structure line
        # The first field, 'character name,' has already been encoded in the string, above.
        # Format of these lines: multiple fields separated by the vertical bar (pipe), since the comma occurs in "character names" in some places:
        # 1. First field is the speaker/actor name, or "STAGE" if it's a stage direction.
        # 2. Remaining fields indicate numbers of sentences in a "chunk," separated by vertical bars.
        #    * A chunk preceded by an opening parenthesis indicates the chunk contains a stage direction.
        while len(to_encode) > 0:
            if '(' in to_encode:                # Then there are parenthetical comments. Sigh.
                if to_encode[0] == '(':
                    structure_code = structure_code + '(%d|' % num_sentences(to_encode[1:to_encode.find(')')])
                    to_encode = to_encode[1+to_encode.find(')'):].strip()
                else:
                    structure_code = structure_code + '%d|' % num_sentences(to_encode[:to_encode.find('(')].strip())
                    to_encode = to_encode[to_encode.find('('):]
            else:
                structure_code = structure_code + '%d' % num_sentences(to_encode)
                to_encode = ""
        structure_code = structure_code.strip().strip('|').strip() + "\n"
        circe_stats_file.write(structure_code)

# OK, write the copora (the structure file has already been written and closed).
for the_name in characters_lines:
    with open(circe_corpora_path + the_name + ".txt", 'w') as current_corpus:
        current_corpus.writelines(characters_lines[the_name])

# OK, that produces 269 files. But only 35 characters speak more than 512 characters' worth of speech.
# Speech from the other 234 is manually combined into the minor characters corpus by moving them into a folder using the Unix `cat` command.

with open(circe_corpora_path + circe_stage_directions_corpus, 'w') as stage_directions_file:
    stage_directions_file.writelines(stage_directions)
