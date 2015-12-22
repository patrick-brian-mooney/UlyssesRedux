#!/usr/bin/env python3
"""Script to set up for a new run of Ulysses Redux. Performs set-up operations."""

import os
import glob
import csv
import subprocess

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations. 

# First, remove the old index file
if os.path.isfile(toc_fragment):
    if input('Delete existing table of contents from last run? ').lower()[0] == 'y':
        os.remove(toc_fragment)

# Set up the data dictionary, using the last run's dictionary keys as a template for this one's
last_run_data = {}.copy()
with open(current_run_data_path, mode='r') as last_run_data_file:
    reader = csv.reader(last_run_data_file)
    last_run_data = {rows[0]:rows[1] for rows in reader}

is_done = False
while not is_done:
    print("\n\nOK, let's set up the parameters for the next run.")
    print("You can type SAME at any prompt to re-use the last run's answer to that question.\n")
    current_run_data = {}.copy()
    for which_key in last_run_data:
        answer = input('%s (previously "%s") ---|  ' % (which_key, last_run_data[which_key]))
        if answer == "SAME":
            current_run_data[which_key] = last_run_data[which_key]
        elif answer != "":
            current_run_data[which_key] = answer
    print('')
    is_done = input("Are you satisfied with that data? ").lower()[0] == 'y'

print('Remember, too, that you can edit %s manually. (Be careful about auto-substitution of smart quotes.)' % current_run_data_path)

# OK, write the new dictionary
with open(current_run_data_path, mode='w') as current_run_data_file:
    writer = csv.writer(current_run_data_file)
    for which_key in current_run_data:
        writer.writerow([which_key, current_run_data[which_key]])

# All right. Check on status of the Git repo.
oldpath = os.getcwd()
try:
    os.chdir(git_repo_path)
    current_git_branch = subprocess.check_output(['git symbolic-ref --short HEAD'], shell=True).decode().split('\n')[0]
    if input ('Current Git branch is "%s". Commit changes, push to remote, and switch to master branch? ' % current_git_branch).lower()[0] == 'y':
        if input('Sync code from working directory first? ').lower()[0] == 'y':
            subprocess.check_call(['/UlyssesRedux/code/utility-scripts/sync-code.sh'], shell=True)
            print('\n\nINFO: OK, synced.')
        subprocess.check_call(['git add -u'], shell=True)
        subprocess.call(['git commit'], shell=True)
        subprocess.check_call(['git push origin %s' % current_git_branch], shell=True)
        subprocess.check_call(['git checkout master'], shell=True)
        print('')
        if input('Merge changes from branch "%s" into master branch? ' % current_git_branch).lower()[0] == 'y':
            subprocess.check_call(['git merge %s' % current_git_branch], shell=True)
    if input('Create and switch to new Git branch? ').lower()[0] == 'y':
        current_episode_number =  1 + int(sorted(glob.glob('%s???.html' % webpage_contents_directory ))[-1][-8:-5])
        branch_name = "%03d" % current_episode_number + current_run_data['current-run-name'].replace(" ", "")
        if input('  use suggested branch name "%s"? ' % branch_name).lower()[0] != 'y':
            branch_name = input('What branch name would you like to use? ')
        subprocess.check_call(['git checkout -b %s' % branch_name], shell=True)
finally:
    os.chdir(oldpath)

# OK, write the 'temporary tags' file
print('Temporary tags used in last run were:')
with open(temporary_tags_file) as old_tags_file:
    print(old_tags_file.read())

new_temporary_tags = [].copy()
is_done = False
while not is_done:
    print('\nEnter new tags, one per line. Hit ENTER on an empty line when finished.')
    empty_line = False
    while not empty_line:
        the_input = input('---| ')
        if the_input == "": empty_line = True
        else: new_temporary_tags.append(the_input + '\n')
    is_done = input('Are you satisfied with this group of tags? ').lower()[0] == 'y'

open(temporary_tags_file, 'w').writelines(new_temporary_tags)

print("\n\nOK, we're done!")
