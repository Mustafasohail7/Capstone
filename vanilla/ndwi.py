import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Paths to Landsat bands (replace with your file paths)
nir_band_path = 'band_data/band3.TIF'
swir_band_path = 'band_data/band5.TIF'

def calculate_ndwi(nir_band, swir_band):
    """
    Calculate Normalized Difference Water Index (NDWI) from NIR and SWIR bands.
    
    Parameters:
    - nir_band: Array representing the Near-Infrared band.
    - swir_band: Array representing the Shortwave Infrared band.
    
    Returns:
    - ndwi: NDWI array.
    """
    ndwi = (nir_band - swir_band) / (nir_band + swir_band)
    return ndwi

def visualize_ndwi(ndwi):
    """
    Visualize NDWI image.
    
    Parameters:
    - ndwi: NDWI array.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(ndwi, cmap='jet')
    plt.colorbar(label='NDWI')
    plt.title('Normalized Difference Water Index (NDWI)')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    plt.show()


# Open bands using rasterio
with rasterio.open(nir_band_path) as nir_src, rasterio.open(swir_band_path) as swir_src:
    # Read band data as numpy arrays
    nir_band = nir_src.read(1)  # Assuming Landsat NIR band is in the first band
    swir_band = swir_src.read(1)  # Assuming Landsat SWIR band is in the first band

    # Calculate NDWI
    ndwi = calculate_ndwi(nir_band, swir_band)

    # Visualize NDWI
    visualize_ndwi(ndwi)
