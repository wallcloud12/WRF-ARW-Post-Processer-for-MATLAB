# WRF-ARW-Post-Processer-for-MATLAB
## Description
  A program that takes WRF-ARW 4D variables and interpolates them to a user specified values.  The user can choose a vertical coordinate of pressure, hieght, and theta.  When the vertical interpolation is complete the data is saved to a .mat file.  This program utilizes the python extension package wrf-python to complete the vertical interpolation and wind component destaggering. 

## Other Needed Python Packages
- numpy
- scipy
- netCDF4
- wrf-python

