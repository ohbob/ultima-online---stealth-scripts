def trial(trial_year: int, trial_month: int, trial_day: int):
    """
    check if set date has passed,
    if it is, remove this file and exit()
    Args:
        trial_day (int):
        trial_month (int):
        trial_year (int):
    """
    import urllib.request
    import urllib.parse
    from datetime import datetime
    import os
    import sys

    url = 'http://worldclockapi.com/api/json/est/now'
    f = urllib.request.urlopen(url)
    response = f.read().decode('utf-8')

    if response:
        date = response.split('"')[7]
        year = int(date.split("T")[0].split("-")[0])
        month = int(date.split("T")[0].split("-")[1])
        day = int(date.split("T")[0].split("-")[2])
        if datetime(year, month, day) > datetime(trial_year, trial_month, trial_day):
            debug("Your trial is over")
            os.remove(sys.argv[0])  # delete this file
            exit()
    else:
        print('Request returned an error.')
        exit()


trial(2021, 1, 12)  # check if the trial is over
