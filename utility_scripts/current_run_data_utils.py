#!/usr/bin/env python3
"""Miscellaneous utils for Ulysses Redux scripts"""

import sys, csv

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

def read_current_run_parameters():
    with open(current_run_data_path) as current_run_data_file:
        reader = csv.reader(current_run_data_file)
        return {rows[0]:rows[1] for rows in reader}

# Format of this dictionary is: keyname that should be in current_run_data -> question to ask if that keyname is missing
expected_keys =    {"current-run-name": "What is the title of the novel that has just been written?",
                    "summary": "Enter a summary description for the current novel:",
                    "ch01desc": "What short description should be used for chapter 1?",
                    "ch02desc": "What short description should be used for chapter 2?",
                    "ch03desc": "What short description should be used for chapter 3?",
                    'ch04desc': "What short description should be used for chapter 4?",
                    'ch05desc': "What short description should be used for chapter 5?",
                    'ch06desc': "What short description should be used for chapter 6?",
                    'ch07desc': "What short description should be used for chapter 7?",
                    'ch08desc': "What short description should be used for chapter 8?",
                    'ch09desc': "What short description should be used for chapter 9?",
                    'ch10desc': "What short description should be used for chapter 10?",
                    'ch11desc': "What short description should be used for chapter 11?",
                    'ch12desc': "What short description should be used for chapter 12?",
                    'ch13desc': "What short description should be used for chapter 13?",
                    'ch14desc': "What short description should be used for chapter 14?",
                    'ch15desc': "What short description should be used for chapter 15?",
                    'ch16desc': "What short description should be used for chapter 16?",
                    'ch17desc': "What short description should be used for chapter 17?",
                    'ch18desc': "What short description should be used for chapter 18?",
                    'ch01tags': "What (comma-separated list of) tags should be used for chapter 1?",
                    'ch02tags': "What (comma-separated list of) tags should be used for chapter 2?",
                    'ch03tags': "What (comma-separated list of) tags should be used for chapter 3?",
                    'ch04tags': "What (comma-separated list of) tags should be used for chapter 4?",
                    'ch05tags': "What (comma-separated list of) tags should be used for chapter 5?",
                    'ch06tags': "What (comma-separated list of) tags should be used for chapter 6?",
                    'ch07tags': "What (comma-separated list of) tags should be used for chapter 7?",
                    'ch08tags': "What (comma-separated list of) tags should be used for chapter 8?",
                    'ch09tags': "What (comma-separated list of) tags should be used for chapter 9?",
                    'ch10tags': "What (comma-separated list of) tags should be used for chapter 10?",
                    'ch11tags': "What (comma-separated list of) tags should be used for chapter 11?",
                    'ch12tags': "What (comma-separated list of) tags should be used for chapter 12?",
                    'ch13tags': "What (comma-separated list of) tags should be used for chapter 13?",
                    'ch14tags': "What (comma-separated list of) tags should be used for chapter 14?",
                    'ch15tags': "What (comma-separated list of) tags should be used for chapter 15?",
                    'ch16tags': "What (comma-separated list of) tags should be used for chapter 16?",
                    'ch17tags': "What (comma-separated list of) tags should be used for chapter 17?",
                    'ch18tags': "What (comma-separated list of) tags should be used for chapter 18?"
                    }

def validate_data():
    current_run_data = read_current_run_parameters()
    # Now let's make sure that the expected data actually IS in the dictionary we've read. Prompt for missing stuff.
    changed_keys = False
    for which_key in list(expected_keys.keys()):
        if which_key not in current_run_data.keys():
            current_run_data[which_key] = input(expected_keys[which_key] + " ")
            changed_keys = True     # Even if it's blank, the key has been added to the dictionary.
        if changed_keys:
            if (input("Write changed dictionary back into data file? ") or "yes"):
                with open(current_run_data_path, 'w') as current_run_data_file:
                    writer = csv.writer(current_run_data_file)
                    for which_key in current_run_data:
                        writer.writerow([which_key, current_run_data[which_key]])
    
if __name__ == "__main__":
    pass
