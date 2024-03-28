"""

This is the wrf run test file. 

"""

#import libraries
import requests
import datetime
import os
import urllib.request 
import time
import pandas as pd
import sys
import shutil
import glob
from subprocess import check_call, STDOUT, CalledProcessError, Popen, PIPE
from datetime import datetime

#Import functions
from functions.config import *
from functions.download_forecast_data_v2 import download_gfs_forecast
from functions.make_daily_run_map import make_run_map

#Download the GFS forecast data - make sure correct download script used, seperate for python 3.10 and 3.11.
download_gfs_forecast()
print(f"After finishing the GFS download, the current time is: {datetime.now().strftime('%H:%M:%S')}")

#Make run map 
make_run_map()
print(f"After making the run map, the current time is: {datetime.now().strftime('%H:%M:%S')}")

#Read the run map
run_map_df = pd.read_csv(run_map_path)

from functions.make_namelists import make_namelists
from functions.get_namelists import get_wps_namelist, get_input_namelist

#Make namelists for WRF 
make_namelists()
print(f"After finishing making the namelists and starting the WRF modelling, the current time is: {datetime.now().strftime('%H:%M:%S')}")

#Run the WRF model
for index, row in run_map_df.iterrows():
    # Progess indicator 
    print("--------------------------------------------------")
    print(f"Running WRF for run {index+1} of {len(run_map_df)}")
    print("--------------------------------------------------\n")

    # loop through all the runs in the run_map, each row is a distinct case for one day of output
    GFS_00 = row['GFS_00_file_path']
    GFS_06 = row['GFS_06_file_path']
    GFS_12 = row['GFS_12_file_path']
    GFS_18 = row['GFS_18_file_path']
    GFS_24 = row['GFS_24_file_path']

    # ---------------------------
    # Copy the namelists
    # ---------------------------
    wps_namelist_file = row['wps_namelist_path']
    wrf_namelist_file = row['wrf_namelist_path']
    get_wps_namelist(wps_namelist_file)
    get_input_namelist(wrf_namelist_file)

    # ---------------------------
    # Run WPS and WPS
    # ---------------------------
    '''
    generate the docker run command for running WRF and WPS - remove -it flag if running via crontab
    '''
    docker_command = f"docker run --rm -v {GEOG_folder}:/home/WRF_WPS/WPS_GEOG -v {GFS_folder}:/home/WRF_WPS/wrfinput -v {OUTPUT_folder}:/home/WRF_WPS/WRF/run/outputs -v {NAMELISTS_folder}:/home/WRF_WPS/wrfinput/namelists wrf_4p4p2_py3"
    process = Popen(docker_command, shell=True)
    process.communicate()

    # ---------------------------
    # Clean up working directory
    # ---------------------------
    # shutil might not over write these do do it manually
    #os.remove(os.path.join(wrf_input_workdir, 'namelist.wps'))
    #os.remove(os.path.join(wrf_input_workdir, 'namelist.input'))    

# clean the GRIB_data directory
#files = glob.glob(os.path.join(GFS_folder, 'gfs*'))
#for i in files:
#    os.remove(i)
