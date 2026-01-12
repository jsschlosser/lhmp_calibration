import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import rcParams
import os
import sys

def run():
	"""
	Takes LHMP dark measurements (in DN) and plots them against temparature. Requires numpy, matplotlib, and pylab.

	"""	
	def collate_datafiles(list_of_files):
		data_list = []
		for file in list_of_files:
			if file.__contains__("Metadata")|file.__contains__("GPS"):
				data = np.loadtxt(file,dtype=str,delimiter=',')
			else:
				data = np.loadtxt(file,delimiter=',')
				
			data_list.append(data)
		return data_list

	fs = 14
	ms = 75 	

	plt.rcParams.update({'font.size': fs})
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']#	

	Data_Files = [f'../Data/{f}' for f in os.listdir(f'../Data')]
	image_data = collate_datafiles(Data_Files)
	Metadata_Files = [f'../Metadata/{f}' for f in os.listdir(f'../Metadata')]
	image_metadata = collate_datafiles(Metadata_Files)
	GPS_Data_Files = [f'../GPS/{f}' for f in os.listdir(f'../GPS')]
	gps_data = collate_datafiles(GPS_Data_Files)
	IMU_Data_Files = [f'../IMU/{f}' for f in os.listdir(f'../IMU')]
	imu_data = collate_datafiles(IMU_Data_Files)

	
	#dict_name = '../Image_Dictionary_1.npy' #input("Enter the file name for analysis: ")	
	#data_file_dictionary = dict_reconfig(np.load(dict_name,allow_pickle='TRUE'))
	image_metadata = np.array(image_metadata)
	image_data = np.array(image_data).astype(float)
	print(image_data[image_data>0])
	sensor_temp = image_metadata[:,-1].astype(float)
	time_avgd_data = np.mean(image_data,axis=(1,2))
	time_stdv_data = np.std(image_data,axis=(1,2))
	rcParams['figure.figsize'] = 5, 3 # W, H
	fig,ax2=plt.subplots(1) # create figure and subplot
	ax2.errorbar(sensor_temp,time_avgd_data, yerr=time_stdv_data, linestyle='none', elinewidth=1.5, ecolor='k', zorder=0, capsize=3.5)
	ax2.plot(sensor_temp,time_avgd_data,marker='o', color='r', linestyle='none', markeredgewidth=1.5, markersize=7.5, markeredgecolor='k', zorder=1)
	ax2.set_xlabel(r"Sensor Temperature ($\degree$C)")
	ax2.set_ylabel(r"Sensor Signal (DN)")
	plt.tight_layout()
	plt.savefig(f"DarkSignal_Temp_plt.jpg", dpi=300)
	#plt.show() # function to display the plot
	plt.close() # 