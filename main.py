# included
import time
import datetime
import os
import json

from constants import *

f'''
A NEW AND REFORMED FILE! THIS WILL LIKELY ALSO GO OUT OF DATE!

Here is the NEW rundown for how this will work.

ON START
    - if DATA_FILEPATH does not exist
        - that means this is the first start. Create the file (in DATA_FILEPATH), and log the current time (using {datetime.datetime.now()})
'''


class Screentime:
    def __init__(self):
        ## set up variables
        # if first start
        self.first_start = False

        # set up all time trackers
        self.tracked_seconds = 0
        self.tracked_minutes = 0
        self.tracked_hours = 0

        # set up interval trackers for logging data
        self.minute_interval_tracker = 0

        # call functions
        self.load_data()
        self.demise()

    def load_data(self):
        if not os.path.exists(DATA_FILEPATH) or not os.path.exists(DATA_FOLDERPATH):
            self.first_start = True
            try: os.mkdir(DATA_FOLDERPATH)
            except: pass
            f = open(DATA_FILEPATH, 'w')
            f.close()
    
    # def save_timekeeper(self):
        

    def demise(self):
        while True:
            self.tracked_seconds += 1
            if self.tracked_seconds >= BASE60_OVERFLOW:
                self.tracked_minutes += 1
                self.minute_interval_tracker += 1
                self.tracked_seconds = 0
            if self.tracked_minutes >= BASE60_OVERFLOW:
                self.tracked_hours += 1
                self.tracked_minutes = 0
            # if self.minute_interval_tracker >= BASE10_OVERFLOW:
            print(f'{self.tracked_seconds}s, {self.tracked_minutes}m, {self.tracked_hours}h')
            time.sleep(1)

            

Screentime()