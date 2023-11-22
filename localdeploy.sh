#!/bin/bash
cd "$(dirname "$0")"
cp /home/joe/snap/firefox/common/.mozilla/firefox/92ur2814.default/places.sqlite databases/firefox.sqlite
python3 export_history.py 
cat _includes/head.html > _site/index.html
cat _site/history.html >> _site/index.html
rm _site/history.html
