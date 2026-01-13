import Raw_Capture
import cv2
import numpy as np 
import raw_data_file_gen
def Run():
	"""
	Simple function for inputting camera settings and acquiring images from the LHMP.
	
	:type wvl: numpy array         
	:return: dictionary of raw image data in digital number along with the image metadata of exposure time (us), gain, acquisition time (UTC), sensor temperature (degC)
	:rtype: numpy dictionary
	"""  

	camera_settings = {}
	camera_settings['acquisition_duration'] = 10
	camera_settings['GainAuto'] = 'Off' #'Continuous' #'Off'
	camera_settings['ExposureAuto'] = 'Off'#'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 157000#5147373
	print(f"Camera Settings: {camera_settings}")
	output_dictionary = Raw_Capture.Run(camera_settings)
	raw_data_file_gen.Run(output_dictionary,'DarkTest.nc')
	#print(f"Output Dictionary: {output}")
	#np.save(f'Image_Dictionary.npy', output) 
	
