# included
import time
import datetime
import os
import json
from sys import exit

# files
from constants import *

# main operating class
class Screentime:
    def __init__(self, SecondSaveInterval: int = 60):
        ## set up variables
        self.debug = True
        self.SecondSaveInterval = SecondSaveInterval

        # set up time tracker
        self.remembrance = {
            START_TIMESTAMP: self.get_timestamp(), # when the data.json was created
            ACCESS_TIMESTAMP: self.get_timestamp(), # updates everytime the program saves data
            TRACKED_SECONDS: 0, # tracks seconds past START_TIMESTAMP - usually set to zero besides when continuing on via SecondSaveInterval
            TRACKED_MINUTES: 0, # tracks minutes past START_TIMESTAMP
            TRACKED_HOURS: 0, # tracked hours past START_TIMESTAMP
            SECOND_INTERVAL_TRACKER: 0, # How many seconds between each save point
            CURRENT_WEEKDAY: datetime.datetime.weekday(datetime.datetime.now()) # tracks the current weekday, responsible for managing day overolls
        }

        # call functions
        self.load_data()
        self.demise() # starts the neverending loop (until it ends)

    # generate timestamp via the datetime library
    def get_timestamp(self) -> str: return datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")

    # save data to a JSON file
    def saveJSON(self, data: any, filepath: str):
        f = open(filepath, 'w')
        json.dump(data, f)
        f.close()

    # load data from a JSON file
    def loadJSON(self, filepath: str) -> any:
        f = open(filepath, 'r')
        data = json.load(f)
        f.close()
        return data

    # loads up data, does formatting
    def load_data(self):
        # if the project folder does not exist, try to make it; fail open
        if not os.path.exists(DATA_FOLDERPATH):
            try: os.mkdir(DATA_FOLDERPATH)
            except: pass
        # if data JSON does not exist, create it with default values
        if not os.path.exists(DATA_FILEPATH): self.saveJSON(self.remembrance, DATA_FILEPATH)
        # load data JSON, set current timestamp, and save data JSON
        else:
            self.remembrance = self.loadJSON(DATA_FILEPATH)
            self.remembrance[ACCESS_TIMESTAMP] = self.get_timestamp()
            self.saveJSON(self.remembrance, DATA_FILEPATH)
        # if daylog JSON does not exist, create it with default values
        if not os.path.exists(DAYLOG_FILEPATH):
            self.saveJSON({'nothing': 'nothing'}, DAYLOG_FILEPATH)
    
    # saves the time keeping dictionary
    def save_timekeeper(self):
        self.remembrance[ACCESS_TIMESTAMP] = self.get_timestamp() # update current timestamp
        self.saveJSON(self.remembrance, DATA_FILEPATH) # save to JSON

    # resets tracked measurements
    def reset_timekeeper(self):
        self.remembrance[TRACKED_SECONDS] = 0
        self.remembrance[TRACKED_MINUTES] = 0
        self.remembrance[TRACKED_HOURS] = 0

    # saves into daylog.json
    def save_daykeeper(self):
        daykeeper = self.loadJSON(DAYLOG_FILEPATH) # load current timekeeper
        daykeeper[self.remembrance[ACCESS_TIMESTAMP]] = self.remembrance # assign current time keeper to the current timestamp
        self.saveJSON(daykeeper, DAYLOG_FILEPATH) # save new daylog to JSON
        self.remembrance[CURRENT_WEEKDAY] = datetime.datetime.weekday(datetime.datetime.now()) # update current weekday
        self.reset_timekeeper() # reset timekeeper

    # main operating loop
    def demise(self):
        while True:
            try:
                # if saved weekday not equal to current fetched weekday, run save daykeeper
                if datetime.datetime.weekday(datetime.datetime.now()) != self.remembrance[CURRENT_WEEKDAY]: self.save_daykeeper()
                # if the exit file exists, delete it then raise keyboardInterrupt
                if os.path.exists(EXIT_FILEPATH):
                    os.remove(EXIT_FILEPATH)
                    raise KeyboardInterrupt
                # increase times, do rollovers
                self.remembrance[TRACKED_SECONDS] += 1
                self.remembrance[SECOND_INTERVAL_TRACKER] += 1
                if self.remembrance[TRACKED_SECONDS] >= BASE60_OVERFLOW: #  overflow seconds to minutes
                    self.remembrance[TRACKED_MINUTES] += 1
                    self.remembrance[TRACKED_SECONDS] = 0
                if self.remembrance[TRACKED_MINUTES] >= BASE60_OVERFLOW: # overflow minutes to hours
                    self.remembrance[TRACKED_HOURS] += 1
                    self.remembrance[TRACKED_MINUTES] = 0
                if self.remembrance[SECOND_INTERVAL_TRACKER] >= self.SecondSaveInterval: # save every (x) seconds, by default 60 seconds
                    self.remembrance[SECOND_INTERVAL_TRACKER] = 0 # reset interval counter
                    self.save_timekeeper() # save the timekeeper file to JSON
                if self.debug: print(f'{self.remembrance[TRACKED_SECONDS]}s, {self.remembrance[TRACKED_MINUTES]}m, {self.remembrance[TRACKED_HOURS]}h, {self.remembrance[CURRENT_WEEKDAY]}, {WEEKDAYS[self.remembrance[CURRENT_WEEKDAY]]}') # just printin
                time.sleep(1)
            except KeyboardInterrupt:
                self.save_timekeeper()
                exit()

if __name__ == '__main__': Screentime()