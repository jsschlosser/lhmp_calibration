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
import IMU_read
import GPS_read
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
    image_data_list = [] # Store acquired images
    image_info_list = [] # Store acquired image meta info (Gain, Exposure Time, Acquisition Time, etc.,)
    GPS_data_list = [] # Store associated GPS data
    IMU_data_list = [] # Store associated IMU data
    IMU_port = '/dev/ttyUSB0' # IMU associated USB serial port linux
    GPS_port = '/dev/ttyUSB1'
    baud = camera_settings['baud']   # set baud rate for IMU and GPS read
    #IMU_ser = serial.Serial(IMU_port, baud, timeout=0.5)
    #GPS_ser = serial.Serial(GPS_port, baud)
    #print("IMU Serial is Opened:", IMU_ser.is_open)
    #print("GPS Serial is Opened:", GPS_ser.is_open)
    if len(devices)>0:
        gps_data = np.array(GPS_read.run())
        gps_data = gps_data[-1,:]
        imu_data = np.array(IMU_read.run())
        imu_data = imu_data[-1,:]
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
        pixel_format_name = 'PolarizedDolp_BayerRG8'
        pixel_format_name = 'BayerRG8'
        
        nodes['PixelFormat'].value = pixel_format_name
        
        start_time = time.time()
        print(f"Starting image acquisition for {camera_settings['acquisition_duration']} seconds...")

        while time.time() - start_time < camera_settings['acquisition_duration']: # Continuously fetch and process images
            with device.start_stream(1):
                #IMU_read.fetch_data()
                #IMU_data_list.append(imu_read.run(IMU_ser).copy())
                #GPS_data_list.append(gps_read.run(GPS_ser).copy())
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
                #image_data_list.append(nparray_reshaped.copy()) # Store the image data
                image_data = nparray_reshaped.copy()
                utc_now = datetime.now(ZoneInfo("UTC"))
                gainvalue = device_nm['GainRaw'].value
                exposuretimevalue = device_nm['ExposureTimeRaw'].value 
                DeviceT = device_nm['DeviceTemperature'].value #
                image_info = np.array([exposuretimevalue, gainvalue, utc_now.strftime('%Y%m%dT%H%M%S-%f'), DeviceT]).astype(str)
                
                # Saving --------------------------------------------------------------
                # RAW
                #png_raw_name = f'Image_{pixel_format_name}_raw_{utc_now.strftime("%Y%m%dT%H%M%S-%f")}.png'
                #cv2.imwrite(png_raw_name, nparray_reshaped)

                # HSV
                #png_hsv_name = f'Image_{pixel_format_name}_hsv_{utc_now.strftime("%Y%m%dT%H%M%S-%f")}.png'
                #cm_nparray = cv2.applyColorMap(nparray_reshaped, cv2.COLORMAP_HSV)
                #cv2.imwrite(png_hsv_name, cm_nparray)
                np.savetxt(f"./Data/Image_data_{image_info[2]}.csv",image_data,delimiter=',',fmt='%s')
                np.savetxt(f"./Metadata/Image_info_{image_info[2]}.csv",image_info.reshape(1,-1),delimiter=',',fmt='%s')
                np.savetxt(f"./GPS/GPS_data_{image_info[2]}.csv",gps_data.reshape(1,-1),delimiter=',',fmt='%s')
                np.savetxt(f"./IMU/IMU_data_{image_info[2]}.csv",imu_data.reshape(1,-1),delimiter=',',fmt='%s')

                device.requeue_buffer(image_buffer)

#    output_dictionary = {}
#    output_dictionary['image_data_list'] = image_data_list
#    output_dictionary['image_info_list'] = image_info_list
#    output_dictionary['GPS_data_list'] = GPS_data
#    output_dictionary['IMU_data_list'] = IMU_data
#    image_data = np.array(image_data_list)
#    image_info = np.array(image_info_list)   
#    np.savetxt(f"./Data/Image_data_list_{image_info[0,2]}-{image_info[-1,2]}.csv",image_data_list,delimiter=',')
#    np.savetxt(f"./Metadata/Image_info_list_{image_info[0,2]}-{image_info[-1,2]}.csv",image_info,delimiter=',')
#    np.savetxt(f"./GPS/GPS_data_list_{image_info[0,2]}-{image_info[-1,2]}.csv",gps_data,delimiter=',')
#    np.savetxt(f"./IMU/IMU_data_list_{image_info[0,2]}-{image_info[-1,2]}.csv",imu_data,delimiter=',')
    #return output_dictionary
