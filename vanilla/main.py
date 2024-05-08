import numpy as np
import sys

from main_helper import *

def main(filepath_1,filepath_2,index,threshold,notebook):
    # blue_band = 2 
    if index==1:
        swir1_band = f'{filepath_1}/B6.TIF'
        swir12_band = f'{filepath_2}/B6.TIF'
        swir2_band = f'{filepath_1}/B7.TIF'
        swir22_band = f'{filepath_2}/B7.TIF'

        swir1 = open_image(swir1_band)
        swir12 = open_image(swir12_band)
        swir2 = open_image(swir2_band)
        swir22 = open_image(swir22_band)

        swir1 = swir1.astype(np.float32)
        swir2 = swir2.astype(np.float32)
        swir12 = swir12.astype(np.float32)
        swir22 = swir22.astype(np.float32)

        swir1,swir12 = same_resize(swir1,swir12)
        swir2,swir22 = same_resize(swir2,swir22)

    green_band = f'{filepath_1}/B3.TIF'
    green2_band = f'{filepath_2}/B3.TIF'
    nir_band = f'{filepath_1}/B5.TIF'
    nir2_band = f'{filepath_2}/B5.TIF'

    green = open_image(green_band)
    green2 = open_image(green2_band)

    nir = open_image(nir_band)
    nir2 = open_image(nir2_band)

    green = green.astype(np.float32)
    nir = nir.astype(np.float32)
    green2 = green2.astype(np.float32)
    nir2 = nir2.astype(np.float32)

    green,green2 = same_resize(green,green2)
    nir,nir2 = same_resize(nir,nir2)

    if index==0:
        img1 = compute_ndwi(green, nir)
        img2 = compute_ndwi(green2, nir2)
    elif index==1:
        img1 = compute_aewi(green, nir, swir1, swir2)
        img2 = compute_aewi(green2, nir2, swir12, swir22)

    # print(img1.shape)
    # visualize(img1,"NDWI before rolling",gray=True,save=True)
    img2 = rollover_image(img2,60)
    # print(img1.shape)
    # visualize(img1,"NDWI after rolling",gray=True,save=True)


    img1_b = binarize_mask(img1,threshold)
    # visualize(img1_b,gray=True)
    img2_b = binarize_mask(img2,threshold)

    diff_image = classify_image(img1_b,img2_b,notebook)

    

    net_water_change = quantify_water_change(diff_image)
    
    net_water_change = net_water_change / 1000

    print(f"Net water change: {net_water_change} m^2")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Invalid number of arguments. Please provide 4 arguments: filepath_1, filepath_2, index, threshold.")
        sys.exit(1)

    filepath_1 = sys.argv[1]
    filepath_2 = sys.argv[2]
    index = int(sys.argv[3])
    threshold = float(sys.argv[4])
    notebook = sys.argv[5] == 'True'

    main(filepath_1, filepath_2, index, threshold,notebook)

