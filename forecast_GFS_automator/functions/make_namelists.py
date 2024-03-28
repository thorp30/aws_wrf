import pandas as pd
import os
import shutil
import sys
sys.path.append('/big/data/ead_modelling_project/3_Meteorological/GFS/forecast_GFS_automator/')

from functions.config import *

# for each row in the run_map, iterate and pass the parameters into the template namelist file.
run_map_df = pd.read_csv(run_map_path)

def make_namelists():
    for index, row in run_map_df.iterrows():
        start_date = row['start_date']
        end_date = row['end_date']

        if index == 0:
            restart = ".false."
        else:
            restart = ".true."
        # ---------------------------
        # WPS namelist
        # ---------------------------
        # read the template
        with open(wps_namelist_template, 'r') as f1:
            lines1 = f1.readlines()
                        
            lines1[lines1.index('start_date = XX,\n')] = f"start_date = '{start_date}_00:00:00', '{start_date}_00:00:00', '{start_date}_00:00:00', '{start_date}_00:00:00',\n"
            
            lines1[lines1.index('end_date = XX,\n')] = f"end_date = '{end_date}_00:00:00', '{end_date}_00:00:00', '{end_date}_00:00:00', '{end_date}_00:00:00',\n"

            # write to a text file called namelist_check.wps_namelist_template
            with open(os.path.join(generated_namelist_folder, f'{index+1}_namelist.wps'), 'w') as f2:
                f2.writelines(lines1)

        # ---------------------------
        # WRF namelist
        # ---------------------------
        # read the template
        start_year = row['start_year']
        start_month = row['start_month']
        start_day = row['start_day']
        start_hour = '00'
        end_year = row['end_year']
        end_month = row['end_month']
        end_day = row['end_day']
        end_hour = '00'
        
        with open(wrf_namelist_template, 'r') as f1:
            lines1 = f1.readlines()
            lines1[lines1.index('start_year = XX,\n')] = f"start_year = {start_year}, {start_year}, {start_year}, {start_year},\n"
            lines1[lines1.index('start_month = XX,\n')] = f"start_month = {start_month}, {start_month}, {start_month}, {start_month},\n"
            lines1[lines1.index('start_day = XX,\n')] = f"start_day = {start_day}, {start_day}, {start_day}, {start_day},\n"
            lines1[lines1.index('start_hour = XX,\n')] = f"start_hour = {start_hour}, {start_hour}, {start_hour}, {start_hour},\n"

            lines1[lines1.index('end_year = XX,\n')] = f"end_year = {end_year}, {end_year}, {end_year}, {end_year},\n"
            lines1[lines1.index('end_month = XX,\n')] = f"end_month = {end_month}, {end_month}, {end_month}, {end_month},\n"
            lines1[lines1.index('end_day = XX,\n')] = f"end_day = {end_day}, {end_day}, {end_day}, {end_day},\n"
            lines1[lines1.index('end_hour = XX,\n')] = f"end_hour = {end_hour}, {end_hour}, {end_hour}, {end_hour},\n"
 
            lines1[lines1.index('restart = XX,\n')] = f"restart = {restart},\n"

            # write to a text file with the number appended to the front
            with open(os.path.join(generated_namelist_folder, f'{index+1}_namelist.input'), 'w') as f2:
                f2.writelines(lines1)
#make_namelists()
