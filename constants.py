from os.path import dirname, abspath

# at what point to increment the next thing
# for example, overflow at 60 seconds to increase minutes by 1
# overflow at 24 hours to increase days by 1
BASE60_OVERFLOW = 60
BASE24_OVERFLOW = 24
BASE31_OVERFLOW = 31
BASE12_OVERFLOW = 12
BASE10_OVERFLOW = 10
BASE5_OVERFLOW = 5
BASE1_OVERFLOW = 1

# all file paths
DATA_FOLDERPATH = f'{dirname(abspath(__file__))}/screentime-local'
DATA_FILEPATH = f'{DATA_FOLDERPATH}\\data.json'
DAYLOG_FILEPATH = f'{DATA_FOLDERPATH}\\daylog.json'
EXIT_FILEPATH = f'{DATA_FOLDERPATH}\\exit.txt'

# making dictionary indexing easier
START_TIMESTAMP = 'start timestamp'
ACCESS_TIMESTAMP = 'current timestamp'
TRACKED_SECONDS = 'tracked seconds'
TRACKED_MINUTES = 'tracked minutes'
TRACKED_HOURS = 'tracked hours'
SECOND_INTERVAL_TRACKER = '30 minute interval tracker'
CURRENT_WEEKDAY = 'current weekday'

# defining all weekdays (and their number values)
SUNDAY = 'sunday'
MONDAY = 'monday'
TUESDAY = 'tuesday'
WEDNESDAY = 'wednesday'
THURSDAY = 'thursday'
FRIDAY = 'friday'
SATURDAY = 'saturday'
WEEKDAYS = {
    0: MONDAY,
    1: TUESDAY,
    2: WEDNESDAY,
    3: THURSDAY,
    4: FRIDAY,
    5: SATURDAY,
    6: SUNDAY
}

# JANUARY = 'january'
# FEBRUARY = 'february'
# MARCH = 'march'
# APRIL = 'april'
# MAY = 'may'
# JUNE = 'june'
# JULY = 'july'
# AUGUST = 'august'
# SEPTEMBER = 'september'
# OCTOBER = 'october'
# NOVEMBER = 'november'
# DECEMBER = 'december'