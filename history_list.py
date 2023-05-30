from entry import Entry
import sqlite3
import time
import sys
import export_history
from pathlib import Path


__TIME_FORMAT = "%d/%m/%y %H:%M"



def main(entry): 
    begin=entry.start_epoch()*1000000
    end=entry.end_epoch()*1000000
    return_me=[]
    data=export_history.get_history_from_database('databases/firefox.sqlite',"firefox",begin,end) 
    for line in export_history.domain_filter(data,True,False):
            time=export_history.convert_to_time_zone(line[0])
            time_string=time.strftime("%H:%M")
            location=line[1].replace("https://","")
            string="{}, {}".format(time_string,location.split('?')[0])
            return_me.append(string)
    return return_me

if __name__ == "__main__":
    history=main(Entry(sys.argv[1]))
    for command in history:
        print(command)
