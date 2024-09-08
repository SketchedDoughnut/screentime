# screentime
Monitors screen time on computer

# setup
Its simple! All you need to do is:
- install from requirements.txt: `pip install -r requirements.txt`
- call on the screentime class: `Screentime()`
- you're done! Enjoy :D

# features
The current features are:
- counting seconds, minutes, and hours
- logging data daily and refreshing values
- logging time data every 5 minutes
- very simple

# usage
To start, just call the class `Screentime()`. This will create a local folder, and files within. <br>
To gracefully shut down the program, just run the file `exitProg.py`. <br>
Logs of each day can be accessed in `screentime-local/daylog.json` <br>
Current day information (logged every minute) can be accessed in `screentime-local/day.json` <br>
