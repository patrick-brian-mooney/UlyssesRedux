#!/usr/bin/env python3
"""Produces a quick .csv file summarizing number of sentences in each paragraph
in a chapter. Makes a lot of assumptions about the structure of the text file,
including one paragraph per line with no blank lines.

use: get_chapter_stats FILE, where FILE is the chapter filename.
"""

filename = sys.argv[1]

the_text = open('/UlyssesRedux/corpora/joyce/ulysses/%s' % filename).read()
indiv_sents = the_text.split('\n')
paragraph_stats_list = []
for which_sent in range(len(indiv_sents)):
    paragraph_stats_list.append([1 + which_sent, len(indiv_sents[which_sent].split("."))])
the_stats_file = open('%s-stats.txt' % filename, 'w')
the_stats_file.write('Paragraph #,# of sentences\n')
for the_para in paragraph_stats_list:
  the_stats_file.write("%d, %d\n" % (the_para[0], the_para[1]) )
the_stats_file.close()

