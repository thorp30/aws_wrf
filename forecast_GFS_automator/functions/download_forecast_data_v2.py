"""

This script downloads the GFS forecast data from the NOAA NOMADS server for today. The data is downloaded in GRIB2 format. Note that version 2 (this file) is for use with Python 3.11.

"""

import datetime
import os
import urllib.request 
import time
import ftplib

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
        os.system(f'mv {GFS_folder}/gdas* {GFS_folder}/ss')

    # Iterate through forecast times
    for forecast_time in forecast_times:
        hostname = 'ftp.ncep.noaa.gov'
        file_path = f'/pub/data/nccf/com/gfs/prod/gfs.{current_date}/00/atmos/gfs.t00z.pgrb2.0p25.{forecast_time}'
      

        if not os.path.exists(GFS_folder):
            print(f"Directory {GFS_folder} does not exist. Creating it.")
            os.makedirs(GFS_folder)

        os.chdir(GFS_folder)
        

        while True:
            try:
                with ftplib.FTP(hostname) as ftp:
                    ftp.login()
                    print(f"Downloading {file_path}...")
                    with open(f'gfs.t00z.pgrb2.0p25.{forecast_time}', 'wb') as fp:
                        ftp.retrbinary('RETR ' + file_path, fp.write)
                break
            except ftplib.all_errors as e:
                print(f'Error when trying to open the URL: {e}')
                print('Retrying after 60 seconds.')
                time.sleep(60)

        

        # Rename the file to include the forecast time
        os.rename(f'gfs.t00z.pgrb2.0p25.{forecast_time}', f'gdas.gfs.pgrb2.0p25.{current_date}.{forecast_time}.grb2')

        print(f'GFS forecast data downloaded successfully for {forecast_time}.')

#download_gfs_forecast()
