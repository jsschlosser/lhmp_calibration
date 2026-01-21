import Raw_Capture
import cv2
import numpy as np 
import raw_data_file_gen
def Run():
	"""
	Function for inputting camera settings and acquiring images from the LHMP. Writes output level 0 data to netCDF file for processing.	

	"""  
	camera_settings = {}
	camera_settings['acquisition_duration'] = 30
	camera_settings['GainAuto'] = 'Off' #'Continuous' 'Off'
	camera_settings['ExposureAuto'] = 'Continuous'#'Continuous' 'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 140000#5147373
	camera_settings['sleep_time'] = 0.1
	pxl_format_list = ['BayerRG8','PolarizedDolp_BayerRG8','PolarizedAolp_BayerRG8']
	for pxl_frmt in pxl_format_list:
		camera_settings['PixelFormat'] = pxl_frmt
		print(f"Camera Settings: {camera_settings}")
		output_dictionary = Raw_Capture.Run(camera_settings)
		raw_data_file_gen.Run(output_dictionary,f'{camera_settings["PixelFormat"]}_test.nc')
