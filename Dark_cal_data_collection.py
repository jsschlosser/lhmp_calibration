import Raw_Capture
import cv2
import numpy as np 
import raw_data_file_gen
def DarkCurrent():
	"""
	Function for inputting camera settings and acquiring images from the LHMP. Writes output level 0 data to netCDF file for processing.

	
	"""  

	camera_settings = {}
	camera_settings['acquisition_duration'] = 600
	camera_settings['GainAuto'] = 'Off' #'Continuous' #'Off'
	camera_settings['ExposureAuto'] = 'Off'#'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 150000#5147373
	camera_settings['sleep_time'] = 5
	camera_settings['PixelFormat'] = 'BayerRG8'
	print(f"Camera Settings: {camera_settings}")
	output_dictionary = Raw_Capture.Run(camera_settings)
	raw_data_file_gen.Run(output_dictionary,'DarkCurrent.nc')


def DarkRead():
	"""
	Function for inputting camera settings and acquiring images from the LHMP. Writes output level 0 data to netCDF file for processing.

	
	"""  

	output_dictionary = {}   
	output_dictionary['image_data_list'] = None
	output_dictionary['image_info_list'] = None
	camera_settings = {}
	camera_settings['acquisition_duration'] = 1
	camera_settings['sleep_time'] = 0.1
	camera_settings['GainAuto'] = 'Off' #'Continuous' #'Off'
	camera_settings['ExposureAuto'] = 'Off'#'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['PixelFormat'] = 'BayerRG8'
	for i1 in np.logspace(np.log10(10000),np.log10(150000),100):
		camera_settings['ExposureTimeSetting'] = int(i1)#5147373
		print(f"Camera Settings: {camera_settings}")
		OP_dict = Raw_Capture.Run(camera_settings)
		for key in OP_dict:
			if output_dictionary[key] is None:
				output_dictionary[key] = OP_dict[key]
			else:
				output_dictionary[key] = np.hstack((output_dictionary[key],OP_dict[key]))


	raw_data_file_gen.Run(output_dictionary,'DarkRead.nc')
