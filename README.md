# WRF-ARW-Post-Processor-for-MATLAB
## Description
  A program that takes WRF-ARW 4D variables and interpolates them to a user specified values.  The user can choose a vertical coordinate of pressure, hieght, and theta.  When the vertical interpolation is complete the data is saved to a .mat file.  This program utilizes the python extension package wrf-python to complete the vertical interpolation and wind component destaggering. 

## Other Needed Python Packages
- numpy
- scipy
- netCDF4
- wrf-python

## How to Use
1. Open the python file in a text editor
2. Change the file location variable to the directory path to your wrfout file.
   - Make sure to add a / at the end of the path
3. Change the filename variable to the name of your wrfout file
4. Change the savelocation variable to the directory you want to save the .mat file in.
5. Change the matfilename variable to the name you want the .mat file to have
   - The .mat extension is added for you
6. Change the fourd_variables_to_interpolate to the 4D variables you want added to your file
   - wrf-python has some special names that can be found at https://wrf-python.readthedocs.io/en/latest/diagnostics.html
7. Change the interp_method variable to the desired vertical coordinate using the wrf variable name
8. Change the interp_levels to the desired vertical levels in the cordinate specifed before
9. Exit text editor and use a python interpreter to run the program
