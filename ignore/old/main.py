# included
import time
import datetime
import os
import json

# external
# (none)

# files
from constants import *

'''
So, here is a rundown on how this works (THIS IS NOW OUT OF DATE OH NO)

On start:
    - dumps epoch day as "start epoch day"
    - dumps epoch day as "current epoch day"
    - sets all tracked numbers to 0 (from seconds to years)
Normal operation:
    - counts by seconds
    - When seconds reaches 60, reset to 0 and upfate minutes by 1
    - When minute interval counter reaches 30 (equal to minutes), dump data into data.json and reset the minute interval counter
    - When minutes reach 60, reset to 0 and update hours by 1
    - If the current epoch day (which is got using refresh_epoch()) is not equal to "current epoch day", 
      transfer the seconds, minutes, and hours to the daily count and reset all of the former,
      then set "current epoch day" to the now current one. Increase the day interval counter by 1. Finally,
      log the day average (total time in hours / 24) to a seperate .json file, which serves as a daily log
'''

class Screentime:
    def __init__(self):
        '''
        This function does not contain any logic, that is delegated to other functions.
        This function is only responsible for assigning variables.
        '''
         # get all epoch times
        self.refresh_epoch()

        # refresh date info
        self.refresh_date(True) # load current date
        self.refresh_date() # load runtime date

        # set up all tracked times
        # tracked times represent the current information being documented
        self.tracked_seconds = self.runtime_date.second
        self.tracked_minutes = 0
        self.tracked_hours = 0
        self.tracked_days = 0
        self.tracked_weeks = 0
        self.tracked_months = 0
        self.tracked_years = 0
        self.days_sum = 0
        self.seconds_sum = 0
        self.sync_seconds = self.tracked_seconds

        # set up interval counters
        self.minute_interval_counter = 0
        self.day_interval_counter = 0

        # set up flags
        self.first_start = False
        
        # set up dictionaries
        self.day_log = {}

        # set up paths
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        self.screentime_path = f'{self.wDir}/screentime-local'
        self.data_path = f'{self.screentime_path}/data.json'
        self.day_log_path = f'{self.screentime_path}/day_log.json'

        # start / load directories
        self.startup_directories()

        # setup the main dictionary for storing data
        self.startup_data()

        # start demise
        self.demise()


    def load_timekeeper(self):
        f = open(self.data_path, 'r')
        self.timekeeper = json.load(f)
        f.close()

    
    def dump_timekeeper(self):
        f = open(self.data_path, 'w')
        json.dump(self.timekeeper, f)
        f.close()
        
    
    def startup_directories(self):
        # make sure screentime-local exists
        if not os.path.exists(self.screentime_path):
            os.mkdir(self.screentime_path)
        
        # if data.json does not exist, first_start = True
        if not os.path.exists(self.data_path):
            self.first_start = True

        # make sure day_log.json exists
        if not os.path.exists(self.day_log_path):
            f = open(self.day_log_path, 'w')
            json.dump(self.day_log, f)
            f.close()


    def startup_data(self):
        if self.first_start:
            self.save_timekeeper(False, self.epoch_days)
            self.dump_timekeeper()
        else:
            self.load_timekeeper()


    def save_timekeeper(self, filedump: bool = True, set_start_epoch = None):
        if set_start_epoch == None:
            start_epoch_day = self.timekeeper['start epoch day'] # we want to preserve the start epoch day
            start_date = self.timekeeper['start date (y/m/d)(h/m/s)']
        else:
            start_epoch_day = set_start_epoch
            start_date = str(datetime.datetime.today())
        self.timekeeper = {
            'start epoch day': start_epoch_day,
            'start date (y/m/d)(h/m/s)': start_date,
            'current epoch day': self.epoch_days,
            'current date (y/m/d)(h/m/s)': str(self.current_date),
            'current day': self.current_day,
            'current month': self.current_month,
            'current weekday': self.current_weekday,
            'seconds': self.tracked_seconds,
            'minutes': self.tracked_minutes, 
            'hours': self.tracked_hours,
            'days': self.tracked_days,
            'day sum (hour)': self.days_sum,
            'day sum (second)': self.seconds_sum,
            'weeks': self.tracked_weeks,
            'months': self.tracked_months,
            'years': self.tracked_years
        }
        if filedump:
            self.dump_timekeeper()


    def refresh_date(self, current: bool = False):
        # get date info # https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date
        if current == False:
            self.runtime_date = datetime.datetime.today()
            self.runtime_weekday = self.runtime_date.weekday()
            self.runtime_month = self.runtime_date.month
            self.runtime_day = self.runtime_date.day
        else:
            self.current_date = datetime.datetime.today()
            self.current_weekday = self.current_date.weekday()
            self.current_month = self.current_date.month
            self.current_day = self.current_date.day 


    def refresh_epoch(self):
        self.epoch_seconds = time.time()
        self.epoch_minutes = self.epoch_seconds / BASE60_OVERFLOW
        self.epoch_hours = self.epoch_minutes / BASE60_OVERFLOW
        self.epoch_days = self.epoch_hours / BASE24_OVERFLOW
        self.epoch_months = self.epoch_days / BASE31_OVERFLOW
        self.epoch_years = self.epoch_months / BASE12_OVERFLOW


    def demise(self):
        '''
        demise is fancy name for the main loop :3
        '''
        while True:
            self.tracked_seconds += 1 # iterate tracked seconds
            
            # all overflow cases
            if self.tracked_seconds >= BASE60_OVERFLOW: # if seconds reach 60
                self.tracked_minutes += 1
                self.minute_interval_counter += 1
                self.tracked_seconds = 0
            if self.tracked_minutes >= BASE60_OVERFLOW: # if minutes reach 60
                self.tracked_hours += 1
                self.tracked_minutes = 0
            if self.tracked_hours >= BASE24_OVERFLOW: # if hours reach 24
                self.tracked_days += 1
                self.tracked_hours = 0
            if self.tracked_days >= BASE31_OVERFLOW: # if days reach 31
                self.tracked_months += 1
                self.tracked_days = 0
            if self.tracked_months >= BASE12_OVERFLOW: # if months reach 12
                self.tracked_years += 1
                self.tracked_months = 0
            
            # all interval cases
            if self.minute_interval_counter >= BASE10_OVERFLOW:
                self.save_timekeeper()
                self.minute_interval_counter = 0

            # any day specific cases
            self.refresh_epoch()
            if round(self.runtime_day) != round(self.timekeeper['current day']):
                self.days_sum = self.timekeeper['day sum (hour)']
                self.days_sum += self.tracked_hours
                self.days_sum += (self.tracked_minutes / 60)
                self.days_sum += ((self.tracked_seconds / 60) / 60)
                self.seconds_sum = self.timekeeper['day sum (second)']
                self.seconds_sum += ((self.tracked_hours * 60) * 60)
                self.seconds_sum += (self.tracked_minutes * 60)
                self.seconds_sum += self.tracked_seconds
                self.seconds_sum -= self.sync_seconds
                self.refresh_date(True)
                self.refresh_date()
                self.save_timekeeper()
                f = open(self.day_log_path, 'r')
                self.day_log = json.load(f)
                f.close()
                day_log_key = str(self.runtime_date)
                self.day_log[day_log_key] = {
                    'seconds': self.tracked_seconds - self.sync_seconds,
                    'minutes': self.tracked_minutes,
                    'hours': self.tracked_hours,
                    'days': self.tracked_hours,
                    'weeks': self.tracked_weeks,
                    'months': self.tracked_months,
                    'years': self.tracked_years
                }
                f = open(self.day_log_path, 'w')
                json.dump(self.day_log, f)
                f.close()


            # save time data to dictionary
            self.save_timekeeper(False)

            # sleep
            time.sleep(1)


SCREENTIME = Screentime()