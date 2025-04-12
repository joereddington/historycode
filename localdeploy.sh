#!/bin/bash
cd "$(dirname "$0")"
cp /home/joe/snap/firefox/common/.mozilla/firefox/p043e9k6.default/places.sqlite databases/firefox.sqlite
source venv/bin/activate
python3 export_history.py 
python3 plot_internet_times.py 
deactivate
cat site/pre.md > site/index.md
cat site/history.html >> site/index.md
rm site/history.html
