#! /bin/bash
# Go to WPS directory
cd /home/WRF_WPS/WPS

# Link the namelist.wps file into the WPS directory
ln -sf /home/WRF_WPS/wrfinput/namelists/namelist.wps

# Run geogrid
./geogrid.exe

# Link grib files for the forecast period
./link_grib.csh /home/WRF_WPS/wrfinput/gdas*

# Link the Vtable
ln -sf /home/WRF_WPS/wrfinput/namelists/Vtable.GFS2 Vtable

# Run ungrib
./ungrib.exe

#Run metgrid
./metgrid.exe >& log.metgrid

#Copy geo_em files into the run directory
cp geo_em* /home/WRF_WPS/WRF/run/outputs

# Go to the WRF run directory
cd /home/WRF_WPS/WRF/run

# Link to the WRF namelist
ln -sf /home/WRF_WPS/wrfinput/namelists/namelist.input

# Link to the met_em* outputs from metgrid
ln -sf /home/WRF_WPS/WPS/met_em* .

# Copy last run restart file into the run directory 
cp /home/WRF_WPS/WRF/run/outputs/wrfrst* /home/WRF_WPS/WRF/run

# Remove last run restart file from output directory
rm /home/WRF_WPS/WRF/run/outputs/wrfrst*

# Run real.exe
mpirun -np 42 --oversubscribe --allow-run-as-root ./real.exe

# Run wrf.exe
mpirun -np 42 --oversubscribe --allow-run-as-root ./wrf.exe

# Copy Restart files into run folder incase of model fail
cp /home/WRF_WPS/WRF/run/wrfrst* /home/WRF_WPS/WRF/run/outputs



