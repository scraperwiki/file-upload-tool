#!/bin/sh

# Work around pip which does not fetch tags (yet)
for d in $(find ~/src/ -maxdepth 1 -mindepth 1 -type d); 
do 
  cd $d; 
  git fetch --tags; 
done

cd
pip install -q --user -r tool/requirements.txt
