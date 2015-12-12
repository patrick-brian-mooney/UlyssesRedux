#!/bin/bash

# Script to copy code from the the directory where scripts are built, tested, and actually used (/UlyssesRedux/code) to the directory where they are
# stored and pushed to GitHub. Along the way, it obfuscates login credentials, which is the main point of this separatation/duplication scheme.

# Everything's hard-coded here.

# Before we get started, remove backup files generated by Bluefish.
find /UlyssesRedux/ -iname "*~" -print0 | xargs -0 /bin/rm
find "/home/patrick/Documents/programming/python projects/UlyssesRedux/" -iname "*~" -print0 | xargs -0 /bin/rm

# OK, sync.
rsync -avv --exclude "__pycache__" --exclude ".git" --exclude "markov-sentence-generator" /UlyssesRedux/code/ "/home/patrick/Documents/programming/python projects/UlyssesRedux/"
echo -e "\n\n"

# Obfuscate the login creds by applying the patch file
patch "/home/patrick/Documents/programming/python projects/UlyssesRedux/daily-script.py" "/home/patrick/Documents/programming/python projects/UlyssesRedux/daily-script.patch"

echo -e "\n\n\nREADY FOR GIT COMMIT AND PUSH, if desired.\n"
