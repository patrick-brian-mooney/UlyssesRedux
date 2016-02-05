#!/usr/bin/env python3
"""Looks at the text of Joyce's 'Circe' chapter and coughs up some basic stats.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

from pprint import pprint
import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

characters_dict = {}
stage_direction_paragraphs = 0

circe_file = open(circe_text_path)
for the_line in circe_file:
    split_line = the_line.split(':')
    if len(split_line) == 1 or the_line[0:4] != the_line[0:4].upper():            # It's a stage direction
        stage_direction_paragraphs += 1
    else:
        try:
            characters_dict[split_line[0]] += 1
        except KeyError:
            characters_dict[split_line[0]] = 1

print("Characters and line counts: ")
pprint(characters_dict)
print("\nNumber of characters with speaking parts: %d." % len(characters_dict))

five_to_nine = {}
for which_key in characters_dict:
    if 5 <= characters_dict[which_key] <= 9:
        five_to_nine[which_key] = characters_dict[which_key]

print("Characters with five to nine lines: %d." % len(five_to_nine))
pprint(five_to_nine)

ten_or_more = {}
for which_key in characters_dict:
    if characters_dict[which_key] >= 10:
        ten_or_more[which_key] = characters_dict[which_key]

print("Characters with ten or more lines: %d." % len(ten_or_more))
pprint(ten_or_more)

print("Number of stage direction paragraphs: %s" % stage_direction_paragraphs)