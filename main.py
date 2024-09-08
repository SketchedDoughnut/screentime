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
            CURRENT_TIMESTAMP: self.get_timestamp(), # updates everytime the program saves data
            TRACKED_SECONDS: 0, # tracks seconds past - usually set to zero besides when continuing on from previous values
            TRACKED_MINUTES: 0, # tracks minutes past
            TRACKED_HOURS: 0, # tracked hours pasted
            SECOND_INTERVAL_TRACKER: 0, # interval counter for saving
            CURRENT_WEEKDAY: datetime.datetime.weekday(datetime.datetime.now()) # tracks the current weekday, responsible for managing day overolls
        }

        # call functions
        self.load_data()
        self.demise()

    # generate datetime timestamp
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
        data_state = os.path.exists(DATA_FILEPATH)
        folder_state = os.path.exists(DATA_FOLDERPATH)
        daylog_state = os.path.exists(DAYLOG_FILEPATH)
        if not folder_state:
            try: os.mkdir(DATA_FOLDERPATH)
            except: pass
        # dump the dictionary made above into JSON
        if not data_state: self.saveJSON(self.remembrance, DATA_FILEPATH)
        # load JSON, update current timestamp, save new JSON
        else:
            self.remembrance = self.loadJSON(DATA_FILEPATH)
            self.remembrance[CURRENT_TIMESTAMP] = self.get_timestamp()
            self.saveJSON(self.remembrance, DATA_FILEPATH)
        if not daylog_state:
            self.saveJSON({'nothing': 'nothing'}, DAYLOG_FILEPATH)
    
    # saves remembrance
    def save_timekeeper(self):
        self.remembrance[CURRENT_TIMESTAMP] = self.get_timestamp() # update current timestamp
        self.saveJSON(self.remembrance, DATA_FILEPATH) # save to JSON

    # resets tracked measurements
    def reset_timekeeper(self):
        self.remembrance[TRACKED_SECONDS] = 0
        self.remembrance[TRACKED_MINUTES] = 0
        self.remembrance[TRACKED_HOURS] = 0

    # saves into daylog.json
    def save_daykeeper(self):
        daykeeper = self.loadJSON(DAYLOG_FILEPATH) # load current daylog
        daykeeper[self.remembrance[CURRENT_TIMESTAMP]] = self.remembrance # assign current remembrance to the current timestamp
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
                if self.remembrance[TRACKED_SECONDS] >= BASE60_OVERFLOW: #  overflow seconds to minute
                    self.remembrance[TRACKED_MINUTES] += 1
                    self.remembrance[TRACKED_SECONDS] = 0
                if self.remembrance[TRACKED_MINUTES] >= BASE60_OVERFLOW: # overflow minutes to hour
                    self.remembrance[TRACKED_HOURS] += 1
                    self.remembrance[TRACKED_MINUTES] = 0
                if self.remembrance[SECOND_INTERVAL_TRACKER] >= self.SecondSaveInterval: # save every (x) seconds
                    self.remembrance[SECOND_INTERVAL_TRACKER] = 0 # reset interval counter
                    self.save_timekeeper() # save the timekeeper file to JSON
                if self.debug: print(f'{self.remembrance[TRACKED_SECONDS]}s, {self.remembrance[TRACKED_MINUTES]}m, {self.remembrance[TRACKED_HOURS]}h, {self.remembrance[CURRENT_WEEKDAY]}, {datetime.datetime.weekday(datetime.datetime.now())}') # just printin
                time.sleep(1)
            except KeyboardInterrupt:
                self.save_timekeeper()
                exit()
if __name__ == '__main__': Screentime()