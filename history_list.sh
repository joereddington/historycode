#!/bin/bash
cd "$(dirname "$0")"
cp /home/joe/snap/firefox/common/.mozilla/firefox/lgcolshm.default/places.sqlite databases/firefox.sqlite
python3 history_list.py "$1"


