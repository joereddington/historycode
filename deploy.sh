#!/bin/bash
cd /home/joe/git/historycode/
./localdeploy.sh
cd site
git commit -a -m "Update"
git push 
