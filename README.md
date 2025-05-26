# export-history

A simple script that exports my firefox history as a webpage. 


There is a [blog post](http://joereddington.com/6530/2018/12/12/experimenting-with-public-internet-history./) that talks about the reasons behind this, and there is also a [live example](https://joereddington.github.io/export-history/)

Currently all urls are stripped down to their domain name unless they appear on 'whitelist.txt' 


* databases
The folder where we put the databases from Firefox and Safari 

* lists
The directory containing various black and whitelists

deploy.sh


* entry.py
* export_history.py
* history_list.py
* history_list.sh
* LICENSE

* localdeploy.sh
* plot_internet_times.py
* __pycache__
* README.md
* site
* test_export_history.py
* venv
* window_whitelist.txt


## TODO 
* Put in a proper folder structure 
* Fix local files bug
* Create an actual test database
* Allow wildcards in whitelist 
* Whitelist google from certain dates
* Write up what all the scripts do here 
* Create the branch that has smartsocial and so on in. 
