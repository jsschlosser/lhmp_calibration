import demosaic
import numpy as np
from netCDF4 import Dataset

def Run(pathto_raw_data_file=None):
	"""
	Function for capturing samples with the LHMP.

	:param pathto_raw_data_file: Path to raw image dataset.
	:type pathto_raw_data_file: string	  
	"""  

	pathto_raw_data_file = '../TestData.nc'
	data = Dataset(pathto_raw_data_file,'r')
	data_dictionary = {}		 
	for key in data.variables.keys():
		vals = data.variables[key][:]
		data_dictionary[key] = np.where(vals == '--', np.nan, vals)

	image_data = data_dictionary['Raw_Signal']
	dataset_length = len(image_data[:,0,0])
	h_pixel_length = len(image_data[0,:,0])
	v_pixel_length = len(image_data[0,0,:])
	outout_dictionary = {}
	outout_dictionary['img_stokes_blue'] = np.zeros((dataset_length,h_pixel_length,v_pixel_length,3))
	outout_dictionary['img_stokes_green'] = np.zeros((dataset_length,h_pixel_length,v_pixel_length,3))
	outout_dictionary['img_stokes_red'] = np.zeros((dataset_length,h_pixel_length,v_pixel_length,3))

	#outout_dictionary['img_dolp_bgr'] = np.zeros((dataset_length,h_pixel_length,v_pixel_length,3))
	#outout_dictionary['img_aolp_bgr'] = np.zeros((dataset_length,h_pixel_length,v_pixel_length,3))

	for i1 in range(0,dataset_length):
		demosaiced_data_products = demosaic.Run(image_data[i1,:,:],i1)
#		for key in outout_dictionary:
#			outout_dictionary[key][i1,:,:,] = demosaiced_data_products[key]