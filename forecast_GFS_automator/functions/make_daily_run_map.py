"""

This script makes a daily run map which will run a 3 day forecast. The run map is saved as a csv, and is read 
by the WRF runner to make the namelists and run the WRF model.

"""

import os
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import shutil
import re
from datetime import datetime, timedelta

from functions.config import *

def make_run_map():

    case_df = pd.DataFrame()   
    run_ids = np.arange(1, 4) # using Julian day
    case_df ['run_id'] = run_ids

    # ---------------------------
    # Get the current date and time, the start and end time for the 3 day forecast and put them into the run map
    # ---------------------------

    now = datetime.now()

    # Get the start and end dates for the 3 day forecast based on the current date
    start_date_day_1 = now.strftime("%Y-%m-%d")
    end_date_day_1 = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    start_date_day_2 = end_date_day_1
    end_date_day_2 = (now + timedelta(days=2)).strftime("%Y-%m-%d")

    start_date_day_3 = end_date_day_2
    end_date_day_3 = (now + timedelta(days=3)).strftime("%Y-%m-%d")

    # put the start and end dates into the df
    case_df['start_date'] = [start_date_day_1, start_date_day_2, start_date_day_3]
    case_df['end_date'] = [end_date_day_1, end_date_day_2, end_date_day_3]

    # ---------------------------
    # Populate the run map with the dates for the GFS data for each run, and the paths to the GFS data 
    # ---------------------------

    case_df['GFS_00_file_path'] = None 
    case_df['GFS_06_file_path'] = None 
    case_df['GFS_12_file_path'] = None 
    case_df['GFS_18_file_path'] = None
    case_df['GFS_24_file_path'] = None

    gfs_file_list =[]

    # get the start and end dates from the gfs files
    for file in os.listdir(GFS_folder):
        if file.endswith(".grb2"):
            gfs_file_list.append(file)

    # sort the list of gfs files in ascending order (by forecast time: f000 -> f072)
    gfs_file_list.sort()

    # Subset the gfs files into 5 files for each day
    day_1_gfs = gfs_file_list[0:5]
    day_2_gfs = gfs_file_list[4:9]
    day_3_gfs = gfs_file_list[8:13]

    # Append GFS path to each file
    day_1_gfs = [GFS_folder + file for file in day_1_gfs]
    day_2_gfs = [GFS_folder + file for file in day_2_gfs]
    day_3_gfs = [GFS_folder + file for file in day_3_gfs]

    # Assign the file paths to the corresponding columns in case_df where run_id equals 1
    case_df.loc[case_df['run_id'] == 1, ['GFS_00_file_path', 'GFS_06_file_path', 'GFS_12_file_path', 'GFS_18_file_path', 'GFS_24_file_path']] = day_1_gfs
    case_df.loc[case_df['run_id'] == 2, ['GFS_00_file_path', 'GFS_06_file_path', 'GFS_12_file_path', 'GFS_18_file_path', 'GFS_24_file_path']] = day_2_gfs
    case_df.loc[case_df['run_id'] == 3, ['GFS_00_file_path', 'GFS_06_file_path', 'GFS_12_file_path', 'GFS_18_file_path', 'GFS_24_file_path']] = day_3_gfs

    # ---------------------------
    # make paths to the namelists
    # ---------------------------

    wrf_namelist_list = []
    wps_namelist_list = []

    for i in range(1, len(case_df)+1):
        wrf_namelist_list.append(f'{generated_namelist_folder}{i}_namelist.input')
        wps_namelist_list.append(f'{generated_namelist_folder}{i}_namelist.wps')

    case_df['wrf_namelist_path'] = wrf_namelist_list
    case_df['wps_namelist_path'] = wps_namelist_list

    # ---------------------------
    # Add the individual components of the start and end dates to the run map, these will be used to make the namelists
    # ---------------------------

    #reconvert the start and end dates to datetime objects
    case_df['start_date'] = pd.to_datetime(case_df['start_date'])
    case_df['end_date'] = pd.to_datetime(case_df['end_date'])

    case_df['start_year'] = case_df['start_date'].apply(lambda x: x.strftime("%Y"))
    case_df['start_month'] = case_df['start_date'].apply(lambda x: x.strftime("%m"))
    case_df['start_day'] = case_df['start_date'].apply(lambda x: x.strftime("%d"))

    case_df['end_year'] = case_df['end_date'].apply(lambda x: x.strftime("%Y"))
    case_df['end_month'] = case_df['end_date'].apply(lambda x: x.strftime("%m"))
    case_df['end_day'] = case_df['end_date'].apply(lambda x: x.strftime("%d"))

    # write the run_map
    case_df.to_csv(run_map_path, index=False)    

#make_run_map()
