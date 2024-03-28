"""

Location to store all config settings for run - this is the single source of truth for all the file/date related variables 
that are used in the WRF run.

"""
#import libraries
import os 

# Location of the main project folder
main_path = '/big/data/ead_modelling_project/3_Meteorological/'

# Location where GFS data will be downloaded to on a daily basis
GFS_folder = os.path.join(main_path,'GFS/forecast_GFS_automator/assets/GFS_data/')

# Location where WRF Geog data will be stored
GEOG_folder = os.path.join(main_path,'WRF/SHARED/GEOG_data/WPS_GEOG/')

# Location where WRF output files are written to
OUTPUT_folder = os.path.join(main_path,'WRF/SHARED/WRF_outputs/WRF_forecast/')

# Location of run specific namelists - these are moved for each run to this location, then removed
NAMELISTS_folder = os.path.join(main_path, "GFS/forecast_GFS_automator/assets/")

#WRF working directories
wrf_input_workdir = os.path.join(main_path, 'GFS/forecast_GFS_automator/assets/')

# Location to WPS namelist template
wps_namelist_template = os.path.join(main_path,'GFS/forecast_GFS_automator/assets/master_namelist.wps')

# Location to WRF namelist template
wrf_namelist_template = os.path.join(main_path,'GFS/forecast_GFS_automator/assets/master_namelist.input')

# Location to WRF namelist folder
generated_namelist_folder = os.path.join(main_path,'GFS/forecast_GFS_automator/assets/generated_namelists/')

# forecast times for 72 hours
forecast_times = ['f000', 'f006', 'f012', 'f018', 'f024', 'f030', 'f036', 'f042', 'f048', 'f054', 'f060', 'f066', 'f072']

# Location to save the run map to 
run_map_path = os.path.join(main_path,'GFS/forecast_GFS_automator/run_map.csv')

