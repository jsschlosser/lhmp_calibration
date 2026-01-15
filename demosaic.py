import cv2
import os
import numpy as np
import polanalyser as pa

def Run(raw_image,img_sufix):
    """
    Takes raw LHMP data and performs demosaicing to achive full resolution. Requires numpy, cv2, os, and polanalyser.   

    :param raw_image: raw image data in H x V format.
    :type raw_image: numpy array with size (H x V)   
    
    """     
    
    outout_dictionary = {}
    # Demosaic the raw image into four polarization channels (0, 45, 90, 135 degrees)
    # The 'pa.COLOR_PolarRGB' option handles the combined RGGB-polarization filter array.
    # The output is a set of 12 full-resolution images (R, G, B for each of the 4 angles).
    img_000_brg, img_045_brg, img_090_brg, img_135_brg = pa.demosaicing(raw_image, pa.COLOR_PolarRGB) 

    # Calculate the Stokes vector per-pixel
    image_list = [img_000_brg, img_045_brg, img_090_brg, img_135_brg]
    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(image_list, angles) 
    outout_dictionary['img_stokes_blue'] = img_stokes[:,:,:,0]
    outout_dictionary['img_stokes_green'] = img_stokes[:,:,:,1]
    outout_dictionary['img_stokes_red'] = img_stokes[:,:,:,2]
    #outout_dictionary['angles'] = angles

    # Convert the Stokes vector to Intensity, DoLP and AoLP
    img_intensity_bgr = pa.cvtStokesToIntensity(img_stokes)
    img_dolp_bgr = pa.cvtStokesToDoLP(img_stokes)
    img_aolp_bgr = pa.cvtStokesToAoLP(img_stokes)
    #return outout_dictionary


    # 4. Visualization (optional)
    # The results (s0, dolp, aolp) are full-resolution images.
    # s0 represents the total intensity (a normal color image).
    s0 = np.sum(img_intensity_bgr,axis=2)
    total_intensity_png_name = f'../LeveL_1_data/S0_total_{img_sufix}.png'
    #cv2.imshow("Total Intensity (S0)", s0)
    cv2.imwrite(total_intensity_png_name, s0)
    i0 = 0
    for color in ['blue','green','red']:
        DOLP_png_name = f'../LeveL_1_data/DOLP_{color}_{img_sufix}.png'
        dolp_mono = np.squeeze(img_dolp_bgr[:,:,i0])
        #print(dolp_mono[dolp_mono>0])
        img_dolp_vis = pa.applyColorToDoP(dolp_mono)
        #cv2.imshow(f"DoLP ({color} channel)", img_dolp_vis)     
        cv2.imwrite(DOLP_png_name, img_dolp_vis)
        AOLP_png_name = f'../LeveL_1_data/AOLP_{color}_{img_sufix}.png'
        aolp_mono =np.squeeze(img_aolp_bgr[:,:,i0])
        img_aolp_vis = pa.applyColorToAoLP(aolp_mono)
        #cv2.imshow("Angle of Linear Polarization (AoLP)", img_aolp_vis)        
        cv2.imwrite(AOLP_png_name, img_aolp_vis)
        
        for i1 in [0,1,2]:
            img_stokes_mono = np.squeeze(img_stokes[:,:,i1,i0])
            stokes_png_name = f'../LeveL_1_data/S{i1}_{color}_{img_sufix}.png'
            cv2.imwrite(stokes_png_name, img_stokes_mono)
        i0 += 1                     

        #img_dolp_vis = pa.applyColorToDoP(img_dolp_bgr)
        #cv2.imshow("Degree of Linear Polarization (DoLP)", img_dolp_vis)        
        # AoLP is typically visualized using a colormap
        #img_aolp_vis = pa.applyColorToAoLP(img_aolp)
        #cv2.imshow("Angle of Linear Polarization (AoLP)", img_aolp_vis)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
