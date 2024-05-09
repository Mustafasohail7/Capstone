import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sys


def compute_ndwi(green, nir):
    """
    Compute NDWI from green and NIR bands.
    
    Parameters:
    - green: Array representing the green band.
    - nir: Array representing the NIR band.
    
    Returns:
    - ndwi: NDWI array.
    """
    ndwi = (green - nir) / (green + nir)
    return ndwi

def compute_aewi(green, nir, swir1, swir2):
    aewi = (4 * (green - swir1)) - (1 * nir) - (2.75 * swir2)
    return aewi


def binarize_mask(image,threshold):
    """
    Binarize mask using a threshold value.
    
    Parameters:
    - image: Image array.
    - threshold: Threshold value.
    
    Returns:
    - mask: Binary mask.
    """
    mask = np.zeros_like(image)
    mask[image >= threshold] = 1
    return mask


def visualize(ndwi,title,gray=False,save=False):
    """
    Visualize NDWI image.
    
    Parameters:
    - ndwi: NDWI array.
    """
    plt.figure()
    if gray:
        plt.imshow(ndwi, cmap='gray')
    else:
        plt.imshow(ndwi, cmap='jet')
    plt.colorbar(label='NDWI')
    plt.title(f'{title}')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    if save:
        plt.savefig(f'images/{title}.jpg')
    else:
        plt.show()
        pass



def same_resize(image1,image2):
    min_rows = min(image1.shape[0], image2.shape[0])
    min_cols = min(image1.shape[1], image2.shape[1])

    image1 = image1[:min_rows, :min_cols]
    image2 = image2[:min_rows, :min_cols]

    return image1,image2

def classify_image(ndwi1,ndwi2,display):
    diff_image = np.zeros_like(ndwi1)

    # Where water has been added (0 in old, 1 in new)
    diff_image[(ndwi1 == 0) & (ndwi2 == 1)] = 0  # Color code: green

    # Where water has been removed (1 in old, 0 in new)
    diff_image[(ndwi1 == 1) & (ndwi2 == 0)] = 1  # Color code: red

    # Where there is no change (0 remains 0)
    diff_image[(ndwi1 == 0) & (ndwi2 == 0)] = 2  # Color code: Yellow

    # Where water remains water (1 remains 1)
    diff_image[(ndwi1 == 1) & (ndwi2 == 1)] = 3  # Color code: blue

    count_green = np.sum(diff_image == 0)
    count_red = np.sum(diff_image == 2)
    count_yellow = np.sum(diff_image == 3)
    count_blue = np.sum(diff_image == 4)

    # original_water = ((count_blue + count_red)*30*30)/(1000*1000)
    # new_water = ((count_blue + count_green)*30*30)/(1000*1000)

    # print(f"Original water: {original_water}")
    # print(f"New water: {new_water}")

    colors = ['red', 'green', 'yellow', 'blue']  # Blue, Green, Red, Yellow
    # colors = [(1, 1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0)]  # Blue, Green, Black, Red
    cmap = ListedColormap(colors)

    mask = np.zeros_like(diff_image)
    mask[diff_image == 2] = 1
    # visualize(mask,"Water change",gray=True)

    plt.figure()
    plt.imshow(diff_image, cmap=cmap)
    plt.colorbar(ticks=[0, 1, 2, 3], label='Change Type')
    plt.title('Change Detection: 1-Removed, 2-Added, 3-No Change, 4-Water Remains')
    if display:
        plt.savefig('difference.jpg')
    else:
        plt.show()
        

    return diff_image

def count_white_pixels(binary_mask):
    """
    Count the number of white pixels in the binary mask.
    
    Parameters:
    - binary_mask: Binary mask.
    
    Returns:
    - count: Number of white pixels.
    """
    count = np.sum(binary_mask == 1)
    count_scaled = count*30*30
    count_scaled_km = count_scaled/(1000*1000)
    return count_scaled_km

def open_image(image_path):
    with rasterio.open(image_path) as src:
        image = src.read(1)
        # meta = src.meta
    return image


def rollover_image(image,rolling_window):
    shifted_img = np.roll(image, -rolling_window, axis=1)

    # Pad the gap on the right with black pixels
    shifted_img[:, -rolling_window:] = 0

    return shifted_img

def save_image(image_path, image_data, meta):
    """
    Save image data to a new TIFF file.
    
    Parameters:
    - image_path: Path to save the new TIFF file.
    - image_data: Image data to be saved.
    - meta: Metadata of the image.
    """
    with rasterio.open(image_path, 'w', **meta) as dst:
        dst.write(image_data, 1)

def quantify_water_change(diff_image):
    # Count the number of pixels classified as water added (green)
    water_added_count = np.sum(diff_image == 0)
    water_added_count = (water_added_count*30*30)

    # Count the number of pixels classified as water removed (red)
    water_removed_count = np.sum(diff_image == 1)
    water_removed_count = (water_removed_count*30*30)

    # Calculate the net change in water by subtracting water_removed_count from water_added_count
    net_water_change = water_removed_count - water_added_count

    return net_water_change

def visualize_band(img,band):
    water_added_mask = (img == band)

    # Create a new array to visualize only the blue pixels
    blue_pixels = np.zeros_like(img, dtype=np.uint8)
    blue_pixels[water_added_mask] = 255  # Set blue pixels to white (255)

    # Visualize the blue pixels
    plt.imshow(blue_pixels, cmap='gray')  # Use cmap='gray' for black and white
    plt.title('Water Added (Blue Pixels)')
    plt.axis('off')
    plt.show()

import csv

def write_to_csv_header(file_path, header):
    """
    Write the header to a CSV file in write mode.

    Args:
    - file_path: The path to the CSV file.
    - header: A list containing the header fields.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
    # print("Header written to", file_path)

def write_to_csv(file_path, data):
    """
    Append data to a CSV file.

    Args:
    - file_path: The path to the CSV file.
    - data: A list containing the data to be written.
    """
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
