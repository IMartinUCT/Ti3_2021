# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 21:25:07 2021

@author: eduar
"""

import cv2
import numpy as np

cr = cv2.imread("celulas.jpg",cv2.IMREAD_GRAYSCALE)

mask = np.zeros((cr.shape), np.uint8)
contour = np.array([[0,320],[640,320],[640,70],[0,80]])

cv2.fillPoly(mask, pts =[contour], color=(255,255,255))

masked_img = cv2.bitwise_and(mask,cr)
gauss = cv2.GaussianBlur(masked_img, (5,5), 0)
_,th = cv2.threshold(gauss,100,150,cv2.THRESH_BINARY)


minDist = 5
param1 = 10 #500
param2 = 20 #200 #smaller value-> more false circles
minRadius = 5
maxRadius = 20 #10

# docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
circles = cv2.HoughCircles(gauss, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(masked_img, (i[0], i[1]), i[2], (0, 255, 0), 2)

# Show result for testing:
cv2.imshow('img', masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""_,th = cv2.threshold(gauss,135,150,cv2.THRESH_BINARY)

contornos1,hierarchy1 = cv2.findContours(th, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

print("He encontrado {} celulas".format(len(contornos1)))
cv2.drawContours(gauss, contornos1, -1, (255,0,0), 2)
cv2.imshow('contornos', th)
cv2.imshow('Celulas', gauss)

cv2.waitKey(0)"""
"""
(0, 80), (640, 70), 255, 1)
"""