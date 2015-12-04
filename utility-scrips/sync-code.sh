#!/bin/bash

# Script to copy code from the the directory where scripts are built, tested, and actually used (/UlyssesRedux/code) to the directory where they are
# stored and pushed to GitHub. Along the way, it obfuscates login credentials, which is the main point of this separatation/duplication scheme.

# Everything's hard-coded here.

find /UlyssesRedux/code/ -iname "*~" -print0 | xargs -0 /bin/rm
rsync -avv --exclude "__pycache__" --exclude ".git" --exclude "markov-sentence-generator" /UlyssesRedux/code/ "/home/patrick/Documents/programming/python projects/UlyssesRedux/"

# Obfuscate the login creds by applying the patch file
patch "/home/patrick/Documents/programming/python projects/UlyssesRedux/daily-script.py" "/home/patrick/Documents/programming/python projects/UlyssesRedux/daily-script.patch"

echo -e "\n\n\nREADY FOR GIT COMMIT AND PUSH, if desired."
