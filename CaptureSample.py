from arena_api.system import system
import os
import time
from pathlib import Path
import cv2
import matplotlib.pyplot as plt 
import numpy as np 
import time
from datetime import date
from datetime import datetime
from zoneinfo import ZoneInfo

import os
def Run(camera_settings):
    """
    Basic function for capturing samples with the LHMP.

    :param camera_settings: dictionary containing the gain and exposure time camera settings as well as the acquisition duration 
    :type camera_settings: numpy dictionary        
    :return: dictionary of raw image data in digital number along with the image metadata of exposure time (us), gain, acquisition time (UTC), sensor temperature (degC)
    :rtype: numpy dictionary
    """  
    devices = system.create_device()

    image_data_list = [] # Store acquired images
    image_info_list = [] # Store acquired image meta info (Gain, Exposure Time, Acquisition Time, etc.,)
    if len(devices)>0:
        start_time = time.time()
        print(f"Starting image acquisition for {camera_settings['acquisition_duration']} seconds...")

        devices = create_devices_with_tries()
        device = system.select_device(devices)  

        tl_stream_nodemap = device.tl_stream_nodemap # Get device stream nodemap   
        tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True # Enable stream auto negotiate packet size
        tl_stream_nodemap['StreamPacketResendEnable'].value = True # Enable stream packet resend
        
        device_nm = device.node_map
        device_nm.GainAuto.value = camera_settings['GainAuto']  #'Continuous'
        if device_nm.GainAuto.value == 'Off':
            device_nm.Gain.value = camera_settings['GainSetting']
        device_nm.ExposureAuto.value = camera_settings['ExposureAuto'] 
        if device_nm.ExposureAuto.value == 'Off':
            device_nm.ExposureTime.value = camera_settings['ExposureTimeSetting']     

        # Get nodes ---------------------------------------------------------------
        nodes = device_nm.get_node(['Width', 'Height', 'PixelFormat']) 

        # Nodes
        nodes['Width'].value = nodes['Width'].max   

        height = nodes['Height']
        height.value = height.max   

        # Set pixel format to 'PolarizedDolp_BayerRG8'
        pixel_format_name = 'PolarizedDolp_BayerRG8'
        nodes['PixelFormat'].value = pixel_format_name

        while time.time() - start_time < camera_settings['acquisition_duration']: # Continuously fetch and process images
            with device.start_stream(1):
                image_buffer = device.get_buffer()  # Optional args         

                """
                np.ctypeslib.as_array() detects that Buffer.pdata is (uint8, c_ubyte)
                type so it interprets each byte as an element.
                For 16Bit images Buffer.pdata must be cast to (uint16, c_ushort)
                using ctypes.cast(). After casting, np.ctypeslib.as_array() can
                interpret every two bytes as one array element (a pixel).
                """
                nparray_reshaped = np.ctypeslib.as_array(image_buffer.pdata,
                                                        (image_buffer.height,
                                                        image_buffer.width))        
                image_data_list.append(nparray_reshaped.copy()) # Store the image data
                utc_now = datetime.now(ZoneInfo("UTC"))
                gainvalue = device_nm.Gain.value
                exposuretimevalue = device_nm.ExposureTime.value 
                DeviceT = device_nm.DeviceTemperature.value #
                image_info_list.append([exposuretimevalue, gainvalue, utc_now.strftime('%Y%m%dT%H%M%S-%f'), DeviceT])
                
                # Saving --------------------------------------------------------------
                # RAW
                png_raw_name = f'from_{pixel_format_name}_raw_to_png_with_opencv.png'
                cv2.imwrite(png_raw_name, nparray_reshaped)

                # HSV
                png_hsv_name = f'from_{pixel_format_name}_hsv_to_png_with_opencv.png'
                cm_nparray = cv2.applyColorMap(nparray_reshaped, cv2.COLORMAP_HSV)
                cv2.imwrite(png_hsv_name, cm_nparray)


        device.requeue_buffer(image_buffer)

    output_dictionary = {}
    output_dictionary['image_data_list'] = image_data_list
    output_dictionary['image_info_list'] = image_info_list
    return output_dictionary
