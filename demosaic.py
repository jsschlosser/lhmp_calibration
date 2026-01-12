import cv2
import os
import numpy as np
import polanalyser as pa

"""
Takes raw LHMP data and performs demosaicing to achive full resolution. Requires numpy, cv2, os, and polanalyser.

""" 

# 1. Load the raw, single-channel mosaiced image
# The input image should be a single channel (grayscale) image where each
# pixel value corresponds to the intensity measured through its specific
# color and polarization filter.
# Replace "your_raw_image.png" with your actual image file path.
Data_Files = [f'./Data/{f}' for f in os.listdir(f'./Data')]
for file in Data_Files:

    img_raw = cv2.imread(file, 0)   
    img_name_in = file.split('_')
    img_sufix = img_name_in[-1]
    # 2. Demosaic the raw image into four polarization channels (0, 45, 90, 135 degrees)
    # The 'pa.COLOR_PolarRGB' option handles the combined RGGB-polarization filter array.
    # The output is a set of 12 full-resolution images (R, G, B for each of the 4 angles).
    img_000_brg, img_045_brg, img_090_brg, img_135_brg = pa.demosaicing(img_raw, pa.COLOR_PolarRGB) 

    # Calculate the Stokes vector per-pixel
    image_list = [img_000_brg, img_045_brg, img_090_brg, img_135_brg]
    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(image_list, angles)  
    
    # Convert the Stokes vector to Intensity, DoLP and AoLP
    img_intensity_bgr = pa.cvtStokesToIntensity(img_stokes)
    img_dolp_bgr = pa.cvtStokesToDoLP(img_stokes)
    img_aolp_bgr = pa.cvtStokesToAoLP(img_stokes)

    # 4. Visualization (optional)
    # The results (s0, dolp, aolp) are full-resolution images.
    # s0 represents the total intensity (a normal color image).
    s0 = np.sum(img_intensity_bgr,axis=2).astype('uint8')
    total_intensity_png_name = f'DemosaicData/S0_total_{img_sufix}'
    #cv2.imshow("Total Intensity (S0)", s0)
    cv2.imwrite(total_intensity_png_name, s0)

    i0 = 0
    for color in ['blue','green','red']:
        DOLP_png_name = f'DemosaicData/DOLP_{color}_{img_sufix}'
        dolp_mono = np.squeeze(img_dolp_bgr[:,:,i0]).astype('uint8')
        #img_dolp_vis = pa.applyColorToDoP(dolp_mono)
        #cv2.imshow(f"DoLP ({color} channel)", img_dolp_vis)     
        cv2.imwrite(DOLP_png_name, dolp_mono)
        AOLP_png_name = f'DemosaicData/AOLP_{color}_{img_sufix}'
        aolp_mono =np.squeeze(img_aolp_bgr[:,:,i0]).astype('uint8')
        cv2.imwrite(AOLP_png_name, aolp_mono)
        
        for i1 in [0,1,2]:
            img_stokes_mono = np.squeeze(img_stokes[:,:,i1,i0])
            stokes_png_name = f'DemosaicData/S{i1}_{color}_{img_sufix}'
            cv2.imwrite(stokes_png_name, img_stokes_mono)
        i0 += 1                 

    #img_dolp_vis = pa.applyColorToDoP(img_dolp_bgr)
    #cv2.imshow("Degree of Linear Polarization (DoLP)", img_dolp_vis)        
    # AoLP is typically visualized using a colormap
    #img_aolp_vis = pa.applyColorToAoLP(img_aolp)
    #cv2.imshow("Angle of Linear Polarization (AoLP)", img_aolp_vis)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
