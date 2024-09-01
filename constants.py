from os.path import dirname, abspath
BASE60_OVERFLOW = 60
BASE24_OVERFLOW = 24
BASE31_OVERFLOW = 31
BASE12_OVERFLOW = 12
BASE10_OVERFLOW = 10
BASE5_OVERFLOW = 5


DATA_FOLDERPATH = f'{dirname(abspath(__file__))}/screentime-local'
DATA_FILEPATH = f'{DATA_FOLDERPATH}\\data.json'
DAYLOG_FILEPATH = f'{DATA_FOLDERPATH}\\daylog.json'
EXIT_FILEPATH = f'{DATA_FOLDERPATH}\\exit.txt'

START_TIMESTAMP = 'start timestamp'
CURRENT_TIMESTAMP = 'current timestamp'
TRACKED_SECONDS = 'tracked seconds'
TRACKED_MINUTES = 'tracked minutes'
TRACKED_HOURS = 'tracked hours'
M30_INTERVAL_TRACKER = '30 minute interval tracker'
CURRENT_WEEKDAY = 'current weekday'

# SUNDAY = 'sunday'
# MONDAY = 'monday'
# TUESDAY = 'tuesday'
# WEDNESDAY = 'wednesday'
# THURSDAY = 'thursday'
# FRIDAY = 'friday'
# SATURDAY = 'saturday'

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
