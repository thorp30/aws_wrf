"""

This script downloads the GFS forecast data from the NOAA NOMADS server for today. The data is downloaded in GRIB2 format. Note that version 1 (this file) is for use with Python 3.10.

"""

import requests
import datetime
import os
import urllib.request 
import time

from functions.config import *

def download_gfs_forecast():
    """
    This function downloads the GFS forecast data from the NOAA server for today. The data is downloaded in GRIB2 format, and 
    saved into the GFS folder directory.
    """
# Get the current date
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # tomorrow's date based on the current date
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")


    # If there are already files in the GFS folder (e.g. downloaded from yesterday), move them to ss folder
    if os.path.exists(GFS_folder):
        os.system(f'mv {GFS_folder}gfs* {GFS_folder}ss')

    # Iterate through forecast times
    for forecast_time in forecast_times:
        # Construct the URL to download the GFS forecast data
        url = f'ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{current_date}/00/atmos/gfs.t00z.pgrb2.0p25.{forecast_time}'

        #change directory to GFS folder - defined in config.py
        os.chdir(GFS_folder)

        #Check if the file exists at the url
        while True:
            try:
                # If the file exists at the URL, urllib.request.urlopen() will not raise an URLError
                urllib.request.urlopen(url)
                break
            except urllib.error.URLError:
                # If the file does not exist at the URL, wait for 60 seconds and then check again
                print(f'File does not exist at {url}. Waiting for 60 seconds.')
                time.sleep(60)
        
        #download the forecast data at url 
        cmd = f'wget {url}'
        os.system(cmd)
        
        # rename the file to include the forecast time
        os.rename(f'gfs.t00z.pgrb2.0p25.{forecast_time}', f'gdas.pgrb2.0p25.{current_date}.{forecast_time}.grb2')

        print(f'GFS forecast data downloaded successfully for {forecast_time}.')

#download_gfs_forecast()
