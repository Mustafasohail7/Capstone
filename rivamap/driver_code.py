import cv2
import numpy as np
import mndwi

B3 = cv2.imread('band_3.TIF',cv2.IMREAD_UNCHANGED)
B5 = cv2.imread('band_5.TIF',cv2.IMREAD_UNCHANGED)

I1 = mndwi.mndwi(B3,B5)
cv2.imwrite("mndwi.TIF", cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX))
