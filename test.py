##############################################
#    Unity WRF Data Vector Field Generator   #
#             Michael P. Vossen              #
#              mpvossen@uwm.edu              #
#               Version 0.1                  #
#       Date Last Worked On: 12/23/2019      #
#                                            #
#               Description:                 #
# A program that creates vector fields for   #
# the Unity game engine using model output   #
# from the Weather Research and Forecasting  #
# model (WRF)                                #
##############################################


#import all the nessisary packages
import numpy as np
import struct
from wrf import getvar, interplevel
from netCDF4 import Dataset
import time

print('Packages Loaded', time.process_time())

##############################################################################

# USER SETTINGS

#the directory path to the WRF out file
filepath = '/home/mpvossen/Data/mpvossen/WRF/test/em_real/'

#name of the WRF out file
wrffilename = 'wrfout_d01_2019-03-11_12:00:00'

# number of vertical levels in the vector field
num_of_levels = 50

#time step in the WRF out file
timestep = 27

#name of the output vector field file
savefilename = 'test2.vf'


##############################################################################

# ACTUAL CODE

#open the WRF out file using netCDF4 becasue the WRF out files are netcdf
rawdata = Dataset(filepath + wrffilename)

#open the u wind variable using the destaggering function in wrf-python becasue
#the U varable in WRF is a staggered grid.
ua = getvar(rawdata, 'ua', timeidx = timestep, meta=False)

#open the v wind variable using the destaggering function in wrf-python becasue
#the V varable in WRF is a staggered grid.
va = getvar(rawdata, 'va', timeidx = timestep, meta=False)

#open the w wind variable using the destaggering function in wrf-python becasue
#the W varable in WRF is a staggered grid.
wa = getvar(rawdata, 'wa', timeidx = timestep, meta=False)

#open the grid height variable using the wrf-python function.
#The height is sperated in base height and pertibation height in the raw file
hgt = getvar(rawdata, 'z', timeidx = timestep, meta=False)

#One problem with WRF out files is that the data uses eta levels for the vertical
#coordinate.  This means it is terrain following and is difficult to visualize.
#(bottom level is ground level everywhere) To fix this the data needs to be 
#adjusted to a vetetical level that is height above sea level for easy visulization.

#allocate space for the new sea level relative vertical coordinates
u = np.zeros((num_of_levels, np.shape(ua)[1], np.shape(ua)[2]))
v = np.zeros((num_of_levels, np.shape(ua)[1], np.shape(ua)[2]))
w = np.zeros((num_of_levels, np.shape(ua)[1], np.shape(ua)[2]))

print("Data Opened", time.process_time())


#find the height of the equally spaced vertical coordinates in meters
levels = np.linspace(0, 14000, num_of_levels)

#go through the wind varables and interpolate them to the specified vertical levels
u[:] = interplevel(ua,hgt, levels,meta=False)
v[:] = interplevel(va,hgt, levels,meta=False)
w[:] = interplevel(wa,hgt, levels,meta=False)

print('Data Postprocessed', time.process_time())

#the resolution of the data. (number of grids contained in one varable after we
#adjust the vertical level)
resolution = np.array([np.shape(u)[0],np.shape(u)[1],np.shape(u)[2]])


#Code below is not fully original and comes partly from another program called
#vectorfields (V 0.1.2).  Adjustment have been made to the orginal code
""" Write the vector field as .vf file format to disk. """
file_handle = open(savefilename, 'wb')
for val in [b'V', b'F', b'_', b'V',
            struct.pack('H', resolution[0]),
            struct.pack('H', resolution[1]),
            struct.pack('H', resolution[2])]:
    file_handle.write(val)

# Layout data in required order.
u_stream = u.flatten('F')
v_stream = v.flatten('F')
w_stream = w.flatten('F')
for i in range(u_stream.size):
    file_handle.write(struct.pack('f', v_stream[i]))
    file_handle.write(struct.pack('f', u_stream[i]))
    file_handle.write(struct.pack('f', w_stream[i]))
file_handle.close()
print("Vector Field Created", time.process_time())