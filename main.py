# included
import time
import datetime
import os
import json
import sys

from constants import *

f'''
A NEW AND REFORMED FILE! THIS WILL LIKELY ALSO GO OUT OF DATE!

Here is the NEW rundown for how this will work.

ON START
    - if DATA_FILEPATH does not exist
        - that means this is the first start. Create the file (in DATA_FILEPATH), and log the current time (using self.get_timestamp())
'''


class Screentime:
    def __init__(self):
        ## set up variables
        # if first start
        # self.first_start = False
        
        # booleans
        self.debug = False

        # set up time tracker
        self.remembrance = {
            START_TIMESTAMP: self.get_timestamp(),
            CURRENT_TIMESTAMP: self.get_timestamp(),
            TRACKED_SECONDS: 0,
            TRACKED_MINUTES: 0,
            TRACKED_HOURS: 0,
            M30_INTERVAL_TRACKER: 0,
            CURRENT_WEEKDAY: datetime.datetime.weekday(datetime.datetime.now())
        }

        # call functions
        self.load_data()
        self.demise()

    def get_timestamp(self) -> str: return datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")

    def saveJSON(self, data: any, filepath: str):
        f = open(filepath, 'w')
        json.dump(data, f)
        f.close()

    def loadJSON(self, filepath: str) -> any:
        f = open(filepath, 'r')
        data = json.load(f)
        f.close()
        return data

    def load_data(self):
        data_state = os.path.exists(DATA_FILEPATH)
        folder_state = os.path.exists(DATA_FOLDERPATH)
        daylog_state = os.path.exists(DAYLOG_FILEPATH)
        # if not data_state or not folder_state or not daylog_state: self.first_start = True
        if not folder_state:
            try: os.mkdir(DATA_FOLDERPATH)
            except: pass
        if not data_state: self.saveJSON(self.remembrance, DATA_FILEPATH)
        else:
            self.remembrance = self.loadJSON(DATA_FILEPATH)
            self.remembrance[CURRENT_TIMESTAMP] = self.get_timestamp()
            self.saveJSON(self.remembrance, DATA_FILEPATH)
        if not daylog_state:
            self.saveJSON({'nothing': 'nothing'}, DAYLOG_FILEPATH)
    
    def save_timekeeper(self):
        self.remembrance[CURRENT_TIMESTAMP] = self.get_timestamp()
        self.saveJSON(self.remembrance, DATA_FILEPATH)

    def reset_timekeeper(self):
        self.remembrance[TRACKED_SECONDS] = 0
        self.remembrance[TRACKED_MINUTES] = 0
        self.remembrance[TRACKED_HOURS] = 0

    def save_daykeeper(self):
        daykeeper = self.loadJSON(DAYLOG_FILEPATH)
        daykeeper[self.remembrance[CURRENT_TIMESTAMP]] = self.remembrance
        self.saveJSON(daykeeper, DAYLOG_FILEPATH)
        self.reset_timekeeper()

    def demise(self):
        while True:
            try:
                if self.debug:
                    if 1 != self.remembrance[CURRENT_WEEKDAY]: 
                        self.save_daykeeper()
                        sys.exit()
                else: 
                    if datetime.datetime.weekday(datetime.datetime.now()) != self.remembrance[CURRENT_WEEKDAY]: self.save_daykeeper()
                self.remembrance[TRACKED_SECONDS] += 1
                if self.remembrance[TRACKED_SECONDS] >= BASE60_OVERFLOW: #  overflow seconds to minute
                    self.remembrance[TRACKED_MINUTES] += 1
                    self.remembrance[M30_INTERVAL_TRACKER] += 1
                    self.remembrance[TRACKED_SECONDS] = 0
                if self.remembrance[TRACKED_MINUTES] >= BASE60_OVERFLOW: # overflow minutes to hour
                    self.remembrance[TRACKED_HOURS] += 1
                    self.remembrance[TRACKED_MINUTES] = 0
                if self.remembrance[M30_INTERVAL_TRACKER] >= BASE10_OVERFLOW: self.save_timekeeper() # overflow interval tracker for saving
                if self.debug: print(f'{self.remembrance[TRACKED_SECONDS]}s, {self.remembrance[TRACKED_MINUTES]}m, {self.remembrance[TRACKED_HOURS]}h') # just printin
                time.sleep(1)
            except KeyboardInterrupt:
                self.save_timekeeper()
                sys.exit()
Screentime()