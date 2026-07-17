#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick hack to combine "characters" text chunks from the Lexically.net corpus
into single files, stripping out XML-style location references, for inclusion
in as rotating source texts in Ulysses Redux. Files processed by this script
can be found at http://lexically.net/wordsmith/support/shakespeare.html.
"""

import os, glob


if __name__ == "__main__":
	os.chdir('/UlyssesRedux/corpora/next run')
	for d in [f for f in glob.glob('*') if os.path.isdir(f)]:
		print(d, end="\t->\t")
		combined_file_name = d[:-11]			# Strip off the "_characters" string
		with open(combined_file_name, mode='w') as comb:
			try:
				old_dir = os.getcwd()
				os.chdir(d)
				for char_file_name in glob.glob('*'):
					with open(char_file_name, encoding='utf_16') as the_char_file:
						the_lines = [ l for l in the_char_file.readlines() if not l.strip().startswith('<') ]
						comb.writelines(the_lines)
			finally:
				os.chdir(old_dir)
