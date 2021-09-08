"""
Created on Mon Sep  6 17:29:20 2021

@author: Enrique
"""

import numpy as np
import cv2 as cv

circles1=0
img = cv.imread('seq/Img000100.jpg')
output = img.copy()
gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
eo = cv.Canny(gray, 50, 250, apertureSize=5)
#cv.imshow('edges', eo)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 1)
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=200, param2=20, minRadius=0, maxRadius=0)
detected_circles = np.uint16(np.around(circles))
for (x, y ,r) in detected_circles[0, :]:
    cv.circle(output, (x, y), r, (0, 0, 0), 2)
    cv.circle(output, (x, y), 2, (255, 255, 255), 2)
    circles1+=1


print ('se han detectado',circles1,'celulas')
cv.imshow('output',output)

cv.waitKey(0)
cv.destroyAllWindows()