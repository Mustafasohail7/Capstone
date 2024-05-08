import rasterio
import matplotlib.pyplot as plt
import numpy as np

def open_image(image_path):
    with rasterio.open(image_path) as src:
        image = src.read(1)
        meta = src.meta
    return image, meta

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

img1,img1_meta = open_image('band_data/b7_1.TIF')
img2,img2_meta = open_image('band_data/b7_2.TIF')

rolling_window = 60

shifted_img = np.roll(img1, -rolling_window, axis=1)

# Pad the gap on the right with black pixels
shifted_img[:, -rolling_window:] = 0
save_image('shifted_and_padded_image.tif', shifted_img, img1_meta)

# visualize(shifted_img, gray=True)