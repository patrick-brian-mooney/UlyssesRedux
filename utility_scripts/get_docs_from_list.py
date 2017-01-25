#!/usr/bin/env python3
"""From a page listing links, download the documents that are linked.

Original inspiration for this script: that douchebag Paul Graham's essay
list at http://paulgraham.com/articles.html.

Usage:
    ./get_docs_from_list.py URL
    
Gets all of the documents linked from the page at URL, not including the page
at URL itself, and downloads them to the directory in directory_structure.py
with the name unsorted_corpus_directory.
"""

import requests, sys, urllib.parse

import html2text        # http://www.aaronsw.com/2002/html2text/

from bs4 import BeautifulSoup

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

if __name__ == "__main__":
    list_page_url = sys.argv[1]
    list_page_html = requests.get(list_page_url).text
    list_page_soup = BeautifulSoup(list_page_html, 'html.parser')
    for which_link in list_page_soup.find_all('a'):
        which_link = which_link.get('href')
        print(which_link)
        individual_page_text = requests.get(urllib.parse.urljoin(list_page_url, which_link)).text
        with open('%s%s' % (unsorted_corpus_directory, which_link), 'w') as essay_file:
            essay_file.write(individual_page_text)
    
