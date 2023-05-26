#!/bin/bash
cd "$(dirname "$0")"
cp /Users/joe/Library/Application\ Support/Firefox/Profiles/er7tx3r3.default-release/places.sqlite databases/firefox.sqlite
python3 export_history.py 
cat _includes/head.html > _site/index.html
cat _site/history.html >> _site/index.html
rm _site/history.html
