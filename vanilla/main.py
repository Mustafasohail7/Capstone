import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define the Landsat bands for NIR (Near Infrared) and SWIR (Shortwave Infrared)
# For Landsat 8: NIR = band 5, SWIR = band 6
# For Landsat 9: NIR = band 5, SWIR = band 7
blue_band = 2 
green_band = 'band_data/band3.TIF'
green2_band = 'band_data/o_band3.TIF'
red_band = 4
nir_band = 'band_data/band5.TIF'
nir2_band = 'band_data/o_band5.TIF'
swir1_band = 'band_data/band6.TIF'
swir12_band = 'band_data/o_band6.TIF'
swir2_band = 'band_data/band7.TIF'
swir22_band = 'band_data/o_band7.TIF'

def open_image(image_path):
    with rasterio.open(image_path) as src:
        image = src.read(1)
    return image

green = open_image(green_band)
green2 = open_image(green2_band)

nir = open_image(nir_band)
nir2 = open_image(nir2_band)

swir1 = open_image(swir1_band)
swir12 = open_image(swir12_band)

swir2 = open_image(swir2_band)
swir22 = open_image(swir22_band)

green = green.astype(np.float32)
nir = nir.astype(np.float32)
swir1 = swir1.astype(np.float32)
swir2 = swir2.astype(np.float32)
green2 = green2.astype(np.float32)
nir2 = nir2.astype(np.float32)
swir12 = swir12.astype(np.float32)
swir22 = swir22.astype(np.float32)

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
    mask[image > threshold] = 1
    return mask

def visualize(ndwi,gray=False):
    """
    Visualize NDWI image.
    
    Parameters:
    - ndwi: NDWI array.
    """
    plt.figure(figsize=(8, 8))
    if gray:
        plt.imshow(ndwi, cmap='gray')
    else:
        plt.imshow(ndwi, cmap='jet')
    plt.colorbar(label='NDWI')
    plt.title('Normalized Difference Water Index (NDWI)')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    plt.show()

def same_resize(image1,image2):
    min_rows = min(image1.shape[0], image2.shape[0])
    min_cols = min(image1.shape[1], image2.shape[1])

    image1 = image1[:min_rows, :min_cols]
    image2 = image2[:min_rows, :min_cols]

    return image1,image2

def classify_image(ndwi1,ndwi2):
    diff_image = np.zeros_like(ndwi1)

    # Where water has been added (0 in old, 1 in new)
    diff_image[(ndwi1 == 0) & (ndwi2 == 1)] = 1  # Color code: Blue

    # Where water has been removed (1 in old, 0 in new)
    diff_image[(ndwi1 == 1) & (ndwi2 == 0)] = 2  # Color code: Green

    # Where there is no change (0 remains 0)
    diff_image[(ndwi1 == 0) & (ndwi2 == 0)] = 3  # Color code: Yellow

    # Where water remains water (1 remains 1)
    diff_image[(ndwi1 == 1) & (ndwi2 == 1)] = 4  # Color code: Red

    colors = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0)]  # Blue, Green, Red, Yellow
    cmap = ListedColormap(colors)

    plt.imshow(diff_image, cmap=cmap, vmin=0, vmax=4)
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label='Change Type')
    plt.title('Change Detection: 1-Added, 2-Removed, 3-Water Remains, 4-No Change')
    plt.show()

    return diff_image

threshold = -25000

green,green2 = same_resize(green,green2)
nir,nir2 = same_resize(nir,nir2)
swir1,swir12 = same_resize(swir1,swir12)
swir2,swir22 = same_resize(swir2,swir22)

# ndwi_1 = compute_ndwi(green, nir)
# ndwi_2 = compute_ndwi(green2, nir2)

aewi_1 = compute_aewi(green, nir, swir1, swir2)
# visualize(aewi_1)
aewi_2 = compute_aewi(green2, nir2, swir12, swir22)

aewi_1_b = binarize_mask(aewi_1,threshold)
aewi_2_b = binarize_mask(aewi_2,threshold)

# visualize(aewi_1_b,gray=True)
# visualize(aewi_2_b,gray=True)


diff_image = classify_image(aewi_1_b,aewi_2_b)

