# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 13:16:41 2015

@author: Leo Isikdogan
Homepage: www.isikdogan.com
Project Homepage: http://live.ece.utexas.edu/research/cne/

Example use of the channel network extraction framework
"""

import cv2
from rivamap import singularity_index, delineate, preprocess, visualization

#You can download the example images from AWS:
#http://landsat-pds.s3.amazonaws.com/L8/138/045/LC81380452015067LGN00/LC81380452015067LGN00_B3.TIF
#http://landsat-pds.s3.amazonaws.com/L8/138/045/LC81380452015067LGN00/LC81380452015067LGN00_B6.TIF

# Read bands 3 and 6 of an example Landsat 8 image
B3 = cv2.imread("../downloads/LC09_L2SP_152042_20240223_20240225_02_T1/L2SR_LC09_L2SP_152042_20240223_20240225_02_T1_SR_B3.TIF", cv2.IMREAD_UNCHANGED)
B6 = cv2.imread("../downloads/LC09_L2SP_152042_20240223_20240225_02_T1/L2SR_LC09_L2SP_152042_20240223_20240225_02_T1_SR_B6.TIF", cv2.IMREAD_UNCHANGED)

# Compute the modified normalized difference water index of the input
I1 = preprocess.mndwi(B3, B6)

# Create the filters that are needed to compute the singularity index
filters = singularity_index.SingularityIndexFilters()

# Compute the modified multiscale singularity index
psi, widthMap, orient = singularity_index.applyMMSI(I1, filters)



# Extract channel centerlines
nms = delineate.extractCenterlines(orient, psi)
centerlines = delineate.thresholdCenterlines(nms)

# Generate a raster map of the extracted channels
raster = visualization.generateRasterMap(centerlines, orient, widthMap)

# Generate a vector map of the extracted channels
visualization.generateVectorMap(centerlines, orient, widthMap, saveDest = "vector.pdf")

# Generate a quiver plot
visualization.quiverPlot(psi, orient, saveDest = "quiver.pdf")

# Save the images that are created at the intermediate steps
cv2.imwrite("mndwi.TIF", cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX))
cv2.imwrite("psi.TIF", cv2.normalize(psi, None, 0, 255, cv2.NORM_MINMAX))
cv2.imwrite("nms.TIF", cv2.normalize(nms, None, 0, 255, cv2.NORM_MINMAX))
cv2.imwrite("centerlines.TIF", centerlines.astype(int)*255)
cv2.imwrite("rasterMap.TIF", cv2.normalize(raster, None, 0, 255, cv2.NORM_MINMAX))
