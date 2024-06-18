#!/bin/bash
cd "$(dirname "$0")"
cp /home/joe/snap/firefox/common/.mozilla/firefox/92ur2814.default/places.sqlite databases/firefox.sqlite
python3 export_history.py 
python3 plot_internet_times.py 
cat site/pre.md > site/index.md
cat site/history.html >> site/index.md
rm site/history.html
