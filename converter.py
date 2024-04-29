

# all imports should go here

import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import show

import skimage.exposure

# access package for AWS access
import boto3

import sys
import os
import subprocess
import datetime
import platform
import datetime

def rasterio_open(f: str) -> rio.io.DatasetReader:
    '''
      rasterio_open: open file path f using rasterio (as rio)
    '''
    return rio.open(f)


# end rasterio_open
fpath = "C:/Users/CC/OneDrive - Habib University/FYP/test/LC08_L2SP_152042_20231010_20231017_02_T1_SR_B4.TIF"
# open Landsat image path 89, row 78
src_image = rasterio_open(fpath)
fig, ax = plt.subplots(1, figsize=(12, 10))
show(src_image, ax=ax)
ax.set_title(
    'Landsat-8 band 4: Pass 0089, row 078 \nLandsat-8 image id: '
    + "helloL"
)
# plt.show()
# convert image to numpy

src_image_array = src_image.read(1)
src_image_array = src_image_array.astype('f4')

# replace zero items (ie array pixels out of image frame) with nan

src_image_array[src_image_array == 0] = np.nan
fig, ax = plt.subplots(1, figsize=(12, 10))
show(src_image_array, ax=ax)
ax.set_title(
    'Landsat-8 band 4: Pass 0089, row 078 \nLandsat-8 image id: '
    + "helloL"
)
# plt.show()
# clean up big data objects

src_image_array = 0
src_image = 0
# Normalize bands into 0.0 - 1.0 scale
def normalize(array):
    '''
    normalize: normalize a numpy array so all value are between 0 and 1
    '''
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)


# end normalize
def make_color_image(b1: int, b2: int, b3: int, fpath: str):
    '''
    make_false_color_image: combine nominated Landsat-8 bands into false color image
    
    Parameters:
    b1, b2, b3 int - values between 1 - 6 (inclusive), being a Landsat-8 band number
    
    fpath str - template for URL to Landsat-8 data
    
    Band Number Description       Wavelength Resolution
    Band 1      Coastal / Aerosol 0.433 to 0.453 µm 30 meter
    Band 2      Visible blue      0.450 to 0.515 µm 30 meter
    Band 3      Visible green     0.525 to 0.600 µm 30 meter
    Band 4      Visible red       0.630 to 0.680 µm 30 meter
    Band 5      Near-infrared     0.845 to 0.885 µm 0 meter
    Band 6      Short wavelength infrared 1.56 to 1.66 µm 30 meter
    
    Environment:
    assumes rasterio imported as rio
    assumes boto package  available for AWS file storage access
    '''

    if not (
        b1 > 0
        and b2 > 0
        and b3 > 0
        and b1 < 7
        and b2 < 7
        and b3 < 7
    ):
        raise ValueError(
            f'One or more invalid Landsat-8 band number {b1}, {b2}, {b3} supplied'
        )
    # endif

    # create URLs for each band
    b1_path = 'C:/Users/CC/OneDrive - Habib University/FYP/test/LC08_L2SP_152042_20231010_20231017_02_T1_SR_B1.TIF'
    b2_path = 'C:/Users/CC/OneDrive - Habib University/FYP/test/LC08_L2SP_152042_20231010_20231017_02_T1_SR_B2.TIF'
    b3_path = 'C:/Users/CC/OneDrive - Habib University/FYP/test/LC08_L2SP_152042_20231010_20231017_02_T1_SR_B3.TIF'

    # open URL with rasterio
    b1 = rio.open(b1_path)
    b2 = rio.open(b2_path)
    b3 = rio.open(b3_path)

    # read into numpy array
    b1_np = b1.read(1)
    b2_np = b2.read(1)
    b3_np = b3.read(1)

    # normalize data to 0<->1
    b1_norm = normalize(b1_np)
    b2_norm = normalize(b2_np)
    b3_norm = normalize(b3_np)

    # create three color image
    rgb = np.dstack((b1_norm, b2_norm, b3_norm))

    return rgb


# end make_color_image

# read true color image
rbg = make_color_image(4, 3, 2, fpath)

fig, ax = plt.subplots(1, figsize=(12, 10))
ax.set_title(
    'Landsat-8 bands 4, 3, 2 True Color: Pass 0089, row 078 \nLandsat-8 image id: '
    + "helloL"
)
# show plot

plt.imshow(rbg)