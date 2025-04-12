#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import csv
import time
import sqlite3
import datetime
import urllib.request, urllib.parse, urllib.error
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import pytz

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




def is_domain_whitelisted(domain, whitelist_domains, match_datetime):
    """
    Check if a domain is whitelisted based on the match date and the date in the file (if present).

    Args:
        domain (str): The domain to check.
        whitelist_domains (dict): A dictionary of whitelisted domains and their associated dates.
        match_date (str): The date from the match (e.g., '2023-01-01').

    Returns:
        bool: True if the domain is whitelisted, False otherwise.
    """
    remove_path = True

    domain_without_comma_date = domain.split(',')[0].strip()

    if domain_without_comma_date in whitelist_domains:
        date_in_file = whitelist_domains[domain_without_comma_date]
        if date_in_file:
            if match_datetime >= date_in_file:
                remove_path = False
        else:
            remove_path = False
            
    return remove_path




def domain_filter(matches, use_blacklist=False, html=True):
    return_me = []
    whitelist_lines = open('lists/whitelist.txt').readlines()

    # Create a dictionary to store whitelisted domains and their associated dates (if present)
    whitelist_domains = {}

    for line in whitelist_lines:
        # Split each line by comma (if present) and take the first part as the domain
        parts = line.split(',')
        domain = parts[0].strip()

        # Check if there is a date (optional)
        date = None
        if len(parts) > 1:
            date = parts[1].strip()
            date = datetime.strptime(date, "%Y-%m-%d")
     

        whitelist_domains[domain] = date

    blacklist = open('lists/blacklist.txt').read().split("\n")

    for row in matches:
        match_datetime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        address_shown = ""
        domain = get_domain(row[1])
        remove_path = True

        if use_blacklist:
            if domain not in blacklist:
                remove_path = False
        else:
            remove_path = is_domain_whitelisted(domain, whitelist_domains,match_datetime)
        if remove_path:
            return_me.append((row[0], domain))
        else:
            ascii_title = ""
            if row[2]:
                ascii_title = row[2]
            if html:
                return_me.append((row[0], "<a href=\"{}\">{}</a>".format(row[1], ascii_title)))
            else:
                return_me.append((row[0], "{} {}".format(row[1], ascii_title)))


    #The below code removes the other pages that appears that the same datestamp
    return_me2 = []
    last_row = ["a", "b"]
    for row in return_me:
        if row[0][:16] == last_row[0][:16]:
            if row[1] == last_row[1]:
                continue
        return_me2.append(row)
        last_row = row

    return return_me2





def most_Common(lst): #from https://stackoverflow.com/a/20872750/170243
    data = Counter(lst)
    return_me="""<h3> Most common sites</h3>
With number of accesses/minutes in parentheses

<ol>"""
    for row in data.most_common()[:30]:
        return_me+="<li>{} ({})</li>\n".format(row[0],row[1])
    return return_me+"""

</ol>"""



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
    with open("site/history.html","w") as html_file:
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
            return "<li class='same'> "+self.time_string+" "+self.location+"</li>\n"
        else:
            return "<li> "+self.time_string+" "+self.location+"</li>\n"


    def __str__(self):
        return "{} {} - {}".format(self.date_string,self.time_string,self.location)

    @property
    def weekday(self):
        return self.time.strftime('%A')
 

def writelist(data,html_file,name=""):
            common_domains=[row[1] for row in domain_filter(data)]
            html_file.write(most_Common(common_domains))
            html_file.write("<H2> Sites and times</H2>\n\n")
            data=domain_filter(data)
            last_vis=Visit(data[0])
            html_file.write("<ul>")
            for row in reversed(data):
                vis=Visit(row)
                delta=last_vis.seconds-vis.seconds

                if last_vis.date_string not in vis.date_string:
                    html_file.write("""</ul>

<H3>{}, {}</H3>

<br>

<ul>""".format(vis.weekday,vis.date_string))
                if delta>1800:
                    html_file.write("""</ul>

<br>

<ul>""")
                to_write=vis.html_out(last_vis)
                html_file.write(to_write)
                last_vis=vis
            html_file.write("</ul>")




def get_window_whitelist(file_path='window_whitelist.txt'):
    # This version allows comments
    with open(file_path, 'r') as file:
        whitelist = []
        for line in file:
            stripped_line = line.split('#', 1)[0].strip()
            if stripped_line:
                whitelist.append(stripped_line)
        return whitelist

def get_daily_access_times(data, timezone='Europe/London', whitelist_file='window_whitelist.txt'):
    # Initialize a dictionary to store the first and last access times for each day
    daily_access = defaultdict(lambda: {'first': None, 'last': None})
    
    # Get the time zone object
    tz = pytz.timezone(timezone)
    
    # Read the whitelist from the file
    whitelist = get_window_whitelist(whitelist_file)
    
    for row in data:
        # Skip entries based on the whitelist
        if any(skip_string in row[1] for skip_string in whitelist):
            continue
        
        # Parse the timestamp and convert to the specified time zone
        utc_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        utc_time = pytz.utc.localize(utc_time)
        local_time = utc_time.astimezone(tz)
        
        # Extract the date and time parts from the local time
        date_str = local_time.strftime('%Y-%m-%d')
        time_str = local_time.strftime('%H:%M:%S')
        
        # Update the first and last access times for the date
        if daily_access[date_str]['first'] is None:
            daily_access[date_str]['first'] = time_str
            daily_access[date_str]['firstsite'] = row[1] #for debugging

        daily_access[date_str]['last'] = time_str
        daily_access[date_str]['lastsite'] = row[1] #for debugging
    
    return daily_access #this is a dictionary with dates as keys

def calculate_total_time(first_time_str, last_time_str, time_format="%H:%M:%S"):
    """
    Calculate the total time between two time strings.

    Args:
        first_time_str (str): The first time string.
        last_time_str (str): The last time string.
        time_format (str): The format of the time strings. Default is "%H:%M:%S".

    Returns:
        str: The total time between the two time strings as a string.
    """
    try:
        first_time = datetime.strptime(first_time_str, time_format)
        last_time = datetime.strptime(last_time_str, time_format)
        
        # Calculate the total time
        total_time = last_time - first_time
        
        # Handle the case where the last time is before the first time (crossing midnight)
        if total_time < timedelta(0):
            total_time += timedelta(days=1)
        
        # Convert the total time to string
        total_time_str = str(total_time)
        return total_time_str
    except ValueError as e:
        return f"Error: {e}"

if __name__=="__main__":
    output_data(get_data_from_database())
    daily_access_times = get_daily_access_times(get_data_from_database())
    with open("site/daily_access_times.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "First Access", "Last Access", "Total Time Online"])
        
        for date, times in daily_access_times.items():
            first_access_str = times['first']
            last_access_str = times['last']

#Debug only            writer.writerow([date, times['firstsite'], first_access_str, last_access_str, calculate_total_time(first_access_str,last_access_str)])
            writer.writerow([date, first_access_str, last_access_str, calculate_total_time(first_access_str,last_access_str)])

