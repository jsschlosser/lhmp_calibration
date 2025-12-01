import CaptureSample
import cv2
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
	camera_settings['ExposureAuto'] = 'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 5147373
	output = CaptureSample.Run(camera_settings)
	print(output)