import CaptureSample
import cv2
import numpy as np 

def Run():
	"""
	Simple function for inputting camera settings and acquiring images from the LHMP.
	
	:type wvl: numpy array         
	:return: dictionary of raw image data in digital number along with the image metadata of exposure time (us), gain, acquisition time (UTC), sensor temperature (degC)
	:rtype: numpy dictionary
	"""  

	camera_settings = {}
	camera_settings['acquisition_duration'] = 60
	camera_settings['GainAuto'] = 'Off' #'Continuous' #'Off'
	camera_settings['ExposureAuto'] = 'Continuous'#'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 2000000#5147373
	camera_settings['baud'] = 9600
	print(f"Camera Settings: {camera_settings}")
	CaptureSample.Run(camera_settings)
	#print(f"Output Dictionary: {output}")
	#np.save(f'Image_Dictionary.npy', output) 
	
