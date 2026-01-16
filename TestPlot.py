import os
import numpy as np
import polanalyser as pa
from netCDF4 import Dataset
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
def DemosaicTest():
	"""
	Function for demosaicing and visualizing DoLP, AoLP, intensity, and the Stoke's vector components.
  
	"""  

	pathto_raw_data_file = '../BayerRG8_test.nc'
	data = Dataset(pathto_raw_data_file,'r')
	data_dictionary = {}		 
	for key in data.variables.keys():
		vals = data.variables[key][:]
		data_dictionary[key] = np.where(vals == '--', np.nan, vals)
	image_data = data_dictionary['Raw_Signal']
	dataset_length = len(image_data[:,0,0])
	h_pixel_length = len(image_data[0,:,0])
	v_pixel_length = len(image_data[0,0,:])
	angles = np.deg2rad([0, 45, 90, 135])
	for i1 in range(0,dataset_length):
		# Demosaic the raw image into four polarization channels (0, 45, 90, 135 degrees)
		# The 'pa.COLOR_PolarRGB' option handles the combined RGGB-polarization filter array.
		# The output is a set of 12 full-resolution images (R, G, B for each of the 4 angles).
		img_000_brg, img_045_brg, img_090_brg, img_135_brg = pa.demosaicing(image_data[i1,:,:], pa.COLOR_PolarRGB) 	
		# Calculate the Stokes vector per-pixel
		image_list = [img_000_brg, img_045_brg, img_090_brg, img_135_brg]
		img_stokes = pa.calcStokes(image_list, angles) 	

		# Convert the Stokes vector to Intensity, DoLP and AoLP
		img_intensity_bgr = pa.cvtStokesToIntensity(img_stokes)
		img_dolp_bgr = pa.cvtStokesToDoLP(img_stokes)
		img_aolp_bgr = pa.cvtStokesToAoLP(img_stokes)	

		# The results (s0, dolp, aolp) are full-resolution images. s0 represents the total intensity (a normal color image).
		s0 = np.sum(img_intensity_bgr,axis=2)
		norm_s0 = mcolors.Normalize(vmin=np.min(s0), vmax=np.max(s0))
		s0_vis = (norm_s0(s0)*255).astype('uint8')
		print(s0_vis)
		total_intensity_png_name = f'../LeveL_1_data/S0_total_{i1}.tiff'
		#cv2.imshow("Total Intensity (S0)", s0)
		cv2.imwrite(total_intensity_png_name, s0_vis)
		DOLP_png_name = f'../LeveL_1_data/DOLP_color_{i1}.tiff'
		AOLP_png_name = f'../LeveL_1_data/AOLP_color_{i1}.tiff'
		img_dolp_vis = (img_dolp_bgr * 255).astype('uint8')
		img_aolp_vis =(img_aolp_bgr * 255).astype('uint8')
				   
		cv2.imwrite(DOLP_png_name, img_dolp_vis)
		cv2.imwrite(AOLP_png_name, img_aolp_vis)
		for i2 in [0,1,2]:
			intensity_png_name = f'../LeveL_1_data/S{i2}_color_{i1}.tiff'
			stks = img_stokes[:,:,:,i2]
			norm_stokes = mcolors.Normalize(vmin=np.min(stks), vmax=np.max(stks))
			img_stokes_vis = (norm_stokes(stks)*255).astype('uint8')
			cv2.imwrite(intensity_png_name, img_stokes_vis)

def standard_test():
	"""
	Function for visualizing standard polarizer DolP.
  
	""" 

	pathto_raw_data_file = '../PolarizedDolp_BayerRG8_test.nc'
	data = Dataset(pathto_raw_data_file,'r')
	data_dictionary = {}		 
	for key in data.variables.keys():
		vals = data.variables[key][:]
		data_dictionary[key] = np.where(vals == '--', np.nan, vals)
	image_data = data_dictionary['Raw_Signal']
	dataset_length = len(image_data[:,0,0])
	h_pixel_length = len(image_data[0,:,0])
	v_pixel_length = len(image_data[0,0,:])
	angles = np.deg2rad([0, 45, 90, 135])
	for i1 in range(0,dataset_length):
		DOLP_png_name = f'../LeveL_1_data/DOLP_standard_{i1}.tiff'
		dolp_mono = np.squeeze(image_data[i1,:,:])
		img_dolp_vis = (dolp_mono * 255).astype('uint8')
		#img_dolp_vis = pa.applyColorToDoP(dolp_mono) 
		cv2.imwrite(DOLP_png_name, dolp_mono)
