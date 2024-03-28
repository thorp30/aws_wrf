from functions.config import wrf_input_workdir
import os
import shutil

def get_wps_namelist(wps_namelist_file):
    """
    Function to copy in the pre-prepared namelist for the case into the working directory
    """
    for src in [wps_namelist_file]:
        wps_dst = wps_namelist_file[-12:]
        
        wps_out = os.path.join(wrf_input_workdir, wps_dst)
        shutil.copy(src, wps_out)    
    return


def get_input_namelist(wrf_namelist_file):
    """
    Function to copy in the pre-prepared namelist for the case into the working directory
    """
    for src in [wrf_namelist_file]:
        wrf_dst = wrf_namelist_file[-14:]

        wrf_out = os.path.join(wrf_input_workdir, wrf_dst)
        shutil.copy(src, wrf_out)
    return




