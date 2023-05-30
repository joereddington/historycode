#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import time
import sqlite3
import datetime
import urllib.request, urllib.parse, urllib.error
from collections import Counter


def get_history_from_database(filename, browser="firefox", start=0,end=0):
    cursor = sqlite3.connect(filename).cursor()
    if browser == "firefox": 
        if start==0:
            cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, title , visit_date FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
        else:  
            cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, title , visit_date FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id and visit_date>{} and visit_date<{}'''.format(start,end))
    elif browser == "safari":
        cursor.execute("SELECT datetime(visit_time + 978307200, 'unixepoch', 'localtime') AS human_readable_time, url, title FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item;")
    else: 
        raise ValueError("Only supports 'firefox' or 'safari' as the browser argument")
    return cursor.fetchall()


def filter_by_date(matches, text): 
    return [x for x in matches if str(text) in str(x[0])]






def get_domain(url):
     if url.startswith("file://"):
        return "Local file"
     return urllib.parse.urlparse(url)[1]   







def domain_filter(matches,use_blacklist=False,html=True):
    return_me=[]
    whitelist=open('lists/whitelist.txt').read().split("\n")
    blacklist=open('lists/blacklist.txt').read().split("\n")
    for row in matches:
        address_shown=""
        domain=get_domain(row[1])
        remove_path=True
        if use_blacklist:
           if domain not in blacklist:
                remove_path=False 
        else:
            if domain in whitelist: 
                remove_path=False 
        

        if remove_path:
            return_me.append((row[0],domain))
        else:
                ascii_title=""
                if row[2]:
                    ascii_title = row[2]
                if html:
                    return_me.append((row[0],"<a href=\"{}\">{}</a>".format(row[1],ascii_title)))
                else:
                    return_me.append((row[0],"{} {}".format(row[1],ascii_title)))
                    

    return_me2=[]
    last_row=["a","b"]
    for row in return_me: 
        if row[0][:16] == last_row[0][:16]:
            if row[1] == last_row[1]:
                continue 
        return_me2.append(row)
        last_row=row
        
    return return_me2


def most_Common(lst): #from https://stackoverflow.com/a/20872750/170243
    data = Counter(lst)
    return_me="<h3> Most common sites</h3>\nWith number of accesses/minutes in parentheses<ol>"
    for row in data.most_common()[:30]:
        return_me+="<li>{} ({})</li>\n".format(row[0],row[1])
    return return_me+"</ol>"

def recent_domains(data):
    dic_domains={}
    for row in data:
        time=convert_to_time_zone(row[0])
        timestamp=time.strftime("%d/%m/%y %H:%M")
        domain=urllib.parse.urlparse(row[1])[1].replace("www.","").replace("mobile.","").replace("m.","")
        dic_domains[domain]=timestamp
    return_me="<h2>How long since?</h2>"
    for key in ['bbc.co.uk','twitter.com','facebook.com','mail.google.com']:
        return_me+="{}: {}<br>\n".format(key,dic_domains[key])
    return return_me


def convert_to_time_zone(time,zone='Europe/London'): 
#convert_to_time_zone("2020-07-25 20:19:07","London") 
    from datetime import datetime
    import pytz
    date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    date = pytz.utc.localize(date)
    return  date.astimezone(pytz.timezone(zone))


def get_data_from_database():
    return sorted(get_history_from_database('databases/firefox.sqlite','firefox'))

def output_data(data):
    with open("_site/history.html","w") as html_file:
        writelist(data, html_file)

class Visit:

    def __init__(self, row):
        self.time=convert_to_time_zone(row[0])
        self.time_string=self.time.strftime("%H:%M")
        self.date_string=self.time.strftime("%d/%m/%y")
        self.location=row[1]
        
    @property 
    def seconds(self):
        return time.mktime(self.time.timetuple())

    def html_out(self,last_vis):
        if (last_vis.location == self.location):
            return "<li class='same'> "+self.time_string+" "+self.location+"\n"
        else:
            return "<li> "+self.time_string+" "+self.location+"\n"


    def __str__(self):
        return "{} {} - {}".format(self.date_string,self.time_string,self.location)

    @property
    def weekday(self):
        return self.time.strftime('%A')
 

def writelist(data,html_file,name=""):
            common_domains=[row[1] for row in domain_filter(data)]
            html_file.write(most_Common(common_domains))
            html_file.write("<H2> Sites and times</H2>")
            data=domain_filter(data)
            last_vis=Visit(data[0])
            html_file.write("<ul>")
            for row in reversed(data):
                vis=Visit(row)
                delta=last_vis.seconds-vis.seconds

                if last_vis.date_string not in vis.date_string:
                    html_file.write("</ul><H3>{}, {}</H3><br><ul>".format(vis.weekday,vis.date_string))
                if delta>1800:
                    html_file.write("</ul><br><ul>")
                to_write=vis.html_out(last_vis)
                html_file.write(to_write)
                last_vis=vis
            html_file.write("</ul>")

if __name__=="__main__":
    output_data(get_data_from_database())
