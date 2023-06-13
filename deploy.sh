#!/bin/bash
cd /home/joe/git/export-history/
./localdeploy.sh
cd _site
git commit -a -m "Update"
git push 
