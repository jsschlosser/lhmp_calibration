import numpy as np 
from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import rcParams
import os
import sys

def run(pathto_raw_dark_cal_data=None):
	"""
	Takes LHMP dark measurements (in DN) and plots them against temparature. Requires numpy, matplotlib, and pylab.

	:param pathto_raw_dark_cal_data: Path to dark calibration dataset.
	:type pathto_raw_dark_cal_data: string		

	"""	
	pathto_raw_dark_cal_data = '../DarkTest_data.nc'
	dark_cal_data = Dataset(pathto_raw_dark_cal_data,'r')
	dark_cal_data_dictionary = {}
	for key in dark_cal_data.variables.keys():
		print(key)
		vals = dark_cal_data.variables[key][:]
		dark_cal_data_dictionary[key] = vals#np.where(vals == '--', np.nan, vals)

	fs =14
	lw = 1.5	
	plt.rcParams.update({'font.size': fs})
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']#	

	
	#dict_name = '../Image_Dictionary_1.npy' #input("Enter the file name for analysis: ")	
	#data_file_dictionary = dict_reconfig(np.load(dict_name,allow_pickle='TRUE'))
	image_data = dark_cal_data_dictionary['Raw_Signal']
	print(image_data[image_data>0])
	sensor_temp = dark_cal_data_dictionary['Detector_Temperature']
	Img_Data = image_data.reshape(len(sensor_temp),-1)
	#time_avgd_data = np.mean(image_data,axis=(1,2))
	#time_stdv_data = np.std(image_data,axis=(1,2))
	rcParams['figure.figsize'] = 5, 3 # W, H
	fig,ax2=plt.subplots(1) # create figure and subplot
	#ax2.errorbar(sensor_temp,time_avgd_data, yerr=time_stdv_data, linestyle='none', elinewidth=1.5, ecolor='k', zorder=0, capsize=3.5)
	#ax2.plot(sensor_temp,time_avgd_data,marker='o', color='r', linestyle='none', markeredgewidth=1.5, markersize=7.5, markeredgecolor='k', zorder=1)
	for i in range(len(sensor_temp)):
		y = Img_Data[i,:]
		x = np.squeeze(sensor_temp[i]*np.ones((1,len(Img_Data[i,:]))))
		ax2.scatter(x[y>0],y[y>0])
	ax2.set_xlabel(r"Sensor Temperature ($\degree$C)")
	ax2.set_ylabel(r"Sensor Signal (DN)")
	ax2.set_ylim(0,np.nanmax(Img_Data,axis=(0,1)))
	plt.tight_layout()
	plt.savefig(f"DarkSignal_Temp_plt.jpg", dpi=300)
	#plt.show() # function to display the plot
	plt.close() # 