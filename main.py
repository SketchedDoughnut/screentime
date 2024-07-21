# included
import time
import os
import json

# external
# (none)

'''
So, here is a rundown on how this works

On start:
    - dumps epoch day as "start epoch day"
    - dumps epoch day as "current epoch day"
    - sets all tracked numbers to 0 (from seconds to years)
Normal operation:
    - counts by seconds
    - When seconds reaches 60, reset to 0 and upate minutes by 1
    - When minute interval counter reaches 30 (equal to minutes), dump data into data.json and reset the minute interval counter
    - When minutes reach 60, reset to 0 and update hours by 1
    - If the current epoch day (which is got using refresh_epoch()) is not equal to "current epoch day", 
      transfer the seconds, minutes, and hours to the daily count and reset all of the former,
      then set "current epoch day" to the now current one. Increase the day interval counter by 1. Finally,
      log the day average (total time in hours / 24) to a seperate .json file, which serves as a daily log
'''

class Screentime:
    def __init__(self):
        # get all epoch times
        self.refresh_epoch()

        # set up all tracked times
        self.tracked_seconds = 0
        self.tracked_minutes = 0
        self.tracked_hours = 0
        self.tracked_days = 0
        self.tracked_weeks = 0
        self.tracked_months = 0
        self.tracked_years = 0

        # set up interval counters
        minute_interval_counter = 0
        day_interval_counter = 0

        # set up flags
        self.first_start = False

        # set up paths
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = f'{self.wDir}/screentime-local/data.json'

    def refresh_epoch(self):
        self.epoch_seconds = time.time()
        self.epoch_minutes = self.epoch_seconds / 60
        self.epoch_hours = self.epoch_minutes / 60
        self.epoch_days = self.epoch_hours / 24
        self.epoch_months = self.epoch_days / 31
        self.epoch_years = self.epoch_months / 12
        self.epoch_days = round(self.epoch_days)
        self.epoch_months = round(self.epoch_months)
        self.epoch_years = round(self.epoch_years)