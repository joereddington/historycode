#!/bin/bash
cd /home/joe/git/historycode/
./localdeploy.sh
cd _site
git commit -a -m "Update"
git push 
