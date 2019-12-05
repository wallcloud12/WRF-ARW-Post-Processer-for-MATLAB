#####################################################
#         WRF-ARW Post Processer for MATLAB         #
#                 Michael Vossen                    #
#             email: mpvossen@uwm.edu               #
#                 Version: 0.1.0                    #
#            Last Worked On: 12/05/2019             #
#                                                   #
#                  Description:                     #
# Program that processes WRF-ARW 4D variables using #
# the wrf-python package then outputs to a .mat     #
# file.  The program also uses wrf-python to        #
# destagger the U, V, and W wind grids.             #
#                                                   #
#####################################################




import numpy as np
import scipy.io as sio
import netCDF4 as nc
from wrf import getvar, interplevel, ALL_TIMES


#file location
filelocation = "E:/NWP/"

#name of wrfout file
filename = "1sim2020_01_01_00_00_00"


#directory path to where the figure will be saved
savelocation = "E:/NWP/"

matfilename = 'sim1'


fourd_variables_to_interpolate = ['tk','td','ua','va','wa']

#Interplation method
#p = pressure
#z = height
#th = theta
interp_method = 'p'

interp_levels = [50000, 30000]

#open netCDF file (ncread)
ncfile = nc.Dataset(filelocation + filename)

#turns array into normal array (masked ones suck)
ncfile.set_always_mask(False)   


#open the precipitable water variable
PWAT = getvar(ncfile,'pw',timeidx=ALL_TIMES, meta=False)
LAT = getvar(ncfile,'XLAT',timeidx=1, meta=False)
LON = getvar(ncfile,'XLONG',timeidx=1, meta=False)

#open the vertical coordinate file
vertical_coord =  getvar(ncfile,interp_method, timeidx=ALL_TIMES, meta=False)


#empty array for opened data
interpdata = np.zeros((len(fourd_variables_to_interpolate), np.shape(vertical_coord)[0], np.shape(vertical_coord)[1], np.shape(vertical_coord)[2],np.shape(vertical_coord)[3]))

#count for index of variables
count = 0
#open data files
for i in fourd_variables_to_interpolate:
    #get all of the variables and put into a 5d array
    interpdata[count,:,:,:,:]= getvar(ncfile,i, timeidx=ALL_TIMES, meta=False)
    #advance forward an index
    count += 1
    print(i)

#create new blank array for interpolated data
#need a new one becasue the number of vertical levels will be different
new_data = np.zeros((np.shape(interpdata)[0], np.shape(interpdata)[1], len(interp_levels), np.shape(interpdata)[3], np.shape(interpdata)[4]))

#loop to interpolate data to desired vertical levels
print('interpolate')
for i in range(0,np.shape(interpdata)[0]):
    #for an index counter again
    #each time start from index 0
    count = 0
    #loop for each vertical level
    for level in interp_levels:
        #interpolate the data
        new_data[i, :, count, :, :] = H850 = interplevel(interpdata[i,:,:,:,:],vertical_coord,level, meta=False)
    print(fourd_variables_to_interpolate[i])



#create the data dictonary
data = {'PWAT':PWAT,'LAT':LAT,'LON':LON}

#add each variable to the data dictionary
for i in range(0,np.shape(new_data)[0]):
    data.update({fourd_variables_to_interpolate[i]:new_data[i,:,:,:,:]})

#save data dictonary to .mat file
sio.savemat(savelocation + matfilename + '.mat', data)

#close netcdf file when finished
ncfile.close()
