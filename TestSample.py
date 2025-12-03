import CaptureSample
import cv2
import matplotlib.pyplot as plt 
import numpy as np 
import time
from datetime import date
from datetime import datetime
from zoneinfo import ZoneInfo

def Run():
	"""
	Simple function for inputting camera settings and acquiring images from the LHMP.
	
	:type wvl: numpy array         
	:return: dictionary of raw image data in digital number along with the image metadata of exposure time (us), gain, acquisition time (UTC), sensor temperature (degC)
	:rtype: numpy dictionary
	"""  

	camera_settings = {}
	acquisition_duration = 10 #seconds
	camera_settings['GainAuto'] = 'Off' #'Continuous' #'Off'
	camera_settings['ExposureAuto'] = 'Continuous'#'Off'
	camera_settings['GainSetting'] = 0
	camera_settings['ExposureTimeSetting'] = 2000000#5147373
	camera_settings['PixelFormat'] = 'PolarizedDolp_BayerRG8'
	print(f"Camera Settings: {camera_settings}")
	start_time = time.time()
	print(f"Starting image acquisition for {camera_settings['acquisition_duration']} seconds...")
	Out_dictionary = {}
	while time.time() - start_time < acquisition_duration: # Continuously fetch and process images
		output = CaptureSample.Run(camera_settings)
		# Saving --------------------------------------------------------------
		# RAW
		measurement_time = output['time']
		png_raw_name = f'Image_{camera_settings['PixelFormat']}_raw_{measurement_time}.png'
		cv2.imwrite(png_raw_name, nparray_reshaped)
		# HSV
		png_hsv_name = f'Image_{camera_settings['PixelFormat']}_hsv_{measurement_time}.png'
		cm_nparray = cv2.applyColorMap(nparray_reshaped, cv2.COLORMAP_HSV)
		cv2.imwrite(png_hsv_name, cm_nparray)
		device.requeue_buffer(image_buffer)
		Out_dictionary[measurement_time] = output
		
	print(f"Output Dictionary: {output}")
