import re
import datetime

class Entry(object):

        def is_today(self):
            if self.date==datetime.datetime.today().date():
                return True
            else:
                return False

        def days_old(self):
            if not self.date: 
                return 999999
            else:
                delta = datetime.date.today() - self.date
                return delta.days


        def is_date(self,input_string):
            match = re.search(r'\d{2}/\d{2}/\d{2}', input_string)
            if match:
                testdate = datetime.datetime.strptime(match.group(), '%d/%m/%y').date()
                if testdate==self.date:
                    return True
                else:
                    return False
            else:
                raise ValueException("Date string is badly formed") 
            return False #should never be here


        def __init__(self, input_string):
          import types
          if isinstance(input_string, str):
            pass
          else: 
            raise ValueError("Input to constructor wasn't a string") 
          try:
            self.input_string=input_string
            match = re.search(r'\d{2}/\d{2}/\d{2}', input_string)
            if match:
                self.date = datetime.datetime.strptime(match.group(), '%d/%m/%y').date()
            else:
                self.date = None
            self.start=None
            self.end=None
            match = re.search(r'(?P<start>\d{2}:\d{2}) to (?P<end>\d{2}:\d{2})', input_string)
            if match:
                self.start = match.group('start')
                self.end = match.group('end')
            else:
                match = re.search(r'(?P<start>\d{2}:\d{2})', input_string)
                if match:
                    self.start = match.group('start')
                    self.end = self.start
                else:
                   raise ValueError("No Start value found on: {}".format(input_string))
            match = re.search(r',\s*(?P<title>.*)', input_string)
            self.title=None
            if match:
                self.title =match.group("title").strip()
            if self.title==None:
                print("Warning: NO title for {}".format(self))
                self.title=""

          except AttributeError as err:
            print("Exception! On this line:")
            print(input_string)
            raise err

        def start_epoch(self):
            time=self.start_datetime()
            epoch = time.timestamp()
            return epoch




        def end_epoch(self):
            time=self.end_datetime()
            epoch = time.timestamp()
            return epoch

        def start_datetime(self):
            from datetime import datetime
            FMT = '%Y-%m-%d%H:%M'
            return datetime.strptime(str(self.date) + self.start, FMT) 
            
        def end_datetime(self):
            if self.end==None:
                self.end=self.start
            from datetime import datetime
            FMT = '%Y-%m-%d%H:%M'
            return datetime.strptime(str(self.date) + self.end, FMT) 

        def get_duration(self):
            #from https://stackoverflow.com/a/3096984/170243
            from datetime import datetime
            FMT = '%H:%M'
            tdelta = datetime.strptime(self.end, FMT) - datetime.strptime(self.start, FMT)
            return tdelta.total_seconds()/60 #returns in minutes



        def __str__(self):
            return self.input_string

