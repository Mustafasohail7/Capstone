import os
import numpy as np

from main_helper import *

def count_folders(directory):
    folder_count = 0
    # Iterate through all items in the directory
    for item in os.listdir(directory):
        # Check if the item is a directory
        if os.path.isdir(os.path.join(directory, item)):
            folder_count += 1
    return folder_count

# Example usage:
directory_path = "downloads"
folders = os.listdir(directory_path)
write_to_csv_header('output.csv',['Date','Water Volume'])
for folder in folders:
    date = folder.split('_')
    date = date[4]
    filepath = os.path.join(directory_path,folder)
    green_band = f'{filepath}/B3.TIF'
    nir_band = f'{filepath}/B5.TIF'

    green = open_image(green_band)
    nir = open_image(nir_band)

    green = green.astype(np.float32)
    nir = nir.astype(np.float32)

    img1 = compute_ndwi(green,nir)

    img1_b = binarize_mask(img1,0.05)

    water_area = count_white_pixels(img1_b)

    print(water_area)

    write_to_csv('output.csv',[date,water_area])