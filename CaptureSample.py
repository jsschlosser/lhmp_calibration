from arena_api.system import system
import os
import time
from pathlib import Path
import numpy as np 
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
    print(devices)
    image_data = {} # Store acquired images as well as meta info (Gain, Exposure Time, Acquisition Time, etc.,)
    if len(devices)>0:
        devices = system.create_device()
        device = system.select_device(devices)  

        tl_stream_nodemap = device.tl_stream_nodemap # Get device stream nodemap   
        tl_stream_nodemap['StreamAutoNegotiatePacketSize'].value = True # Enable stream auto negotiate packet size
        tl_stream_nodemap['StreamPacketResendEnable'].value = True # Enable stream packet resend
        
        device_nm = device.nodemap
        device_nm['GainAuto'].value = camera_settings['GainAuto']  #'Continuous'
        if device_nm['GainAuto'].value == 'Off':
            device_nm['GainRaw'].value = camera_settings['GainSetting']
        device_nm['ExposureAuto'] .value = camera_settings['ExposureAuto'] 
        if device_nm['ExposureAuto'] .value == 'Off':
            device_nm['ExposureTimeRaw'].value = camera_settings['ExposureTimeSetting']     
            device_nm['ExposureTimeRaw'].value = camera_settings['ExposureTimeSetting']     

        # Get nodes ---------------------------------------------------------------
        nodes = device_nm.get_node(['Width', 'Height', 'PixelFormat']) 

        # Nodes
        nodes['Width'].value = nodes['Width'].max   

        height = nodes['Height']
        height.value = height.max   

        # Set pixel format to 'PolarizedDolp_BayerRG8'
        pixel_format_name = camera_settings['PixelFormat']
        nodes['PixelFormat'].value = pixel_format_name

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
            image_data['raw'] = nparray_reshaped # Store the image data
            image_data['time_UTC'] = datetime.now(ZoneInfo("UTC"))
            image_data['gain'] = device_nm['GainRaw'].value
            image_data['exposure_time_s'] = device_nm['ExposureTimeRaw'].value 
            image_data['temperature_C'] = device_nm['DeviceTemperature'].value #
        
    return image_data
