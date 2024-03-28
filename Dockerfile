# base OS
FROM ubuntu:focal

# root user for installs
USER root

# set so we don't get asked questions all the way through
ARG DEBIAN_FRONTEND=noninteractive

# install OS libs
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    bc \
    build-essential \
    bzip2 \
    ca-certificates \
    csh \
    curl \
    file \
    g++ \
    gfortran \
    git \
    less \
    libcurl4-gnutls-dev \
    libhdf5-dev \
    libnetcdf-dev \
    libnetcdff-dev \
    libopenmpi-dev \
    libpng-dev \
    libswitch-perl \
    libssl-dev \
    libxml2-dev \
    locales \
    m4 \
    make \
    nano \
    netcdf-bin \
    ncl-ncarg \
    openmpi-bin \
    openssh-client \
    python3 \
    python-dev \
    python3-pip \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    libproj-dev \
    tcsh \
    valgrind \ 
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/* 

RUN apt-get install python3-pip

ENV CPLUS_INCLUDE_PATH="/usr/include/gdal"
ENV C_INCLUDE_PATH="/usr/include/gdal"

RUN pip3 install setuptools \ 
    && pip3 install wheel \
    && pip3 install numpy==1.22.1 \
    && pip3 install pandas==1.3.5 \
    && pip3 install six==1.16.0 \
    && pip3 install scipy \
    && pip3 install Pillow \
    && pip3 install matplotlib \
    && pip3 install gdal \
    && pip3 install pyproj==3.3.0 \
    && pip3 install fiona==1.8.20 \
    && pip3 install shapely==1.8.0 \
    && pip3 install cython==0.29.26 \
    && pip3 install geopandas==0.10.2 \
    && pip3 install rasterio \
    && pip3 install tifffile \
    && pip3 install folium \
    && pip3 install pandas \
    && pip3 install seaborn \
    && pip3 install rasterio \ 
    && pip3 install rioxarray \
    && pip3 install jupyterlab \
    && pip3 install notebook \
    && pip3 install basemap \
    && pip3 install scikit-learn \ 
    && pip3 install colorama \
    && pip3 install mapclassify \
    && pip3 install netcdf4

RUN locale-gen en_US.UTF-8    

ENV LANG=en_US.UTF-8 
ENV LC_ALL=en_US.UTF-8

# NetCDF installs

# Install netCDF-C
ENV LIB_DIR=/usr/local
ENV HDF5_DIR=/usr/lib/x86_64-linux-gnu/hdf5/serial
ENV HDF5_PATH=/usr/lib/x86_64-linux-gnu/hdf5/serial

RUN NETCDF_C_VERSION="4.4.1.1" \
    && wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-${NETCDF_C_VERSION}.tar.gz -P /tmp \
    && tar -xf /tmp/netcdf-${NETCDF_C_VERSION}.tar.gz -C /tmp \
    && cd /tmp/netcdf-${NETCDF_C_VERSION} \
    && CPPFLAGS=-I${HDF5_DIR}/include LDFLAGS=-L${HDF5_DIR}/lib ./configure --prefix=${LIB_DIR} \
    && make \
    && make install \
    && rm -rf /tmp/netcdf* 
    
# Install netCDF-Fortran
ENV LD_LIBRARY_PATH=${LIB_DIR}/lib
RUN NETCDF_F_VERSION="4.4.4" \
    && wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-${NETCDF_F_VERSION}.tar.gz -P /tmp \
    && tar -xf /tmp/netcdf-fortran-${NETCDF_F_VERSION}.tar.gz -C /tmp \
    && cd /tmp/netcdf-fortran-${NETCDF_F_VERSION} \
    && CPPFLAGS=-I${LIB_DIR}/include LDFLAGS=-L${LIB_DIR}/lib ./configure --prefix=${LIB_DIR} \
    && make \
    && make install \
    && rm -rf /tmp/netcdf*

# Install jasper to support grib2
ENV JASPERLIB=/usr/grib2/lib
ENV JASPERINC=/usr/grib2/include

RUN wget https://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.29.tar.gz \
    && tar -xvf jasper-1.900.29.tar.gz \ 
    && cd jasper-1.900.29 \
    && ./configure --prefix=/usr/grib2 \
    && make \
    && make install 

RUN chmod -R 777 /home/

## WRF and WPS installs
ARG WRF_VERSION="4.4.2"
ARG WPS_VERSION="4.4"

WORKDIR /home/WRF_WPS

RUN wget https://github.com/wrf-model/WRF/releases/download/v${WRF_VERSION}/v${WRF_VERSION}.tar.gz \
        && tar -zxf v${WRF_VERSION}.tar.gz \
        && mv WRFV${WRF_VERSION} WRF \
        && rm v${WRF_VERSION}.tar.gz

RUN wget https://github.com/wrf-model/WPS/archive/v${WPS_VERSION}.tar.gz \
	      && tar -zxf v${WPS_VERSION}.tar.gz \
        && mv WPS-${WPS_VERSION} WPS \
	      && rm v${WPS_VERSION}.tar.gz

# Set paths to required libraries
ENV NETCDF=/usr/local
ENV NETCDF_classic=1

# Set WRF-Chem environment variables
ENV WRF_CHEM=1

# Build WRF first, required for WPS
WORKDIR /home/WRF_WPS/WRF
RUN printf '34\n1\n' | ./configure \
        && ./compile em_real | tee compile.log

# Build WPS second after WRF is built
WORKDIR /home/WRF_WPS/WPS
RUN printf '1\n' | ./configure \
        && ./compile | tee compile.log

RUN chmod -R 777 /home/WRF_WPS

################################################################
# Need to make this dir and make it writable to export files out.
RUN mkdir /home/WRF_WPS/WRF/run/outputs \
    &&chmod -R 777 /home/WRF_WPS/WRF/run/outputs

RUN mkdir /home/WRF_WPS/wrfinput  \
    && mkdir /home/WRF_WPS/wrfinput/namelists \ 
    &&chmod -R 777 /home/WRF_WPS/wrfinput/namelists

# added these to keep Jasper happy
ENV LD_LIBRARY_PATH=/usr/grib2/lib:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/grib2/include:$LD_LIBRARY_PATH

WORKDIR /home/WRF_WPS
COPY init.sh /home/WRF_WPS/init.sh
RUN chmod 755 /home/WRF_WPS/init.sh
CMD /home/WRF_WPS/init.sh

