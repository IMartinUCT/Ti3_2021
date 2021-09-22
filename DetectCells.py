# -*- coding: utf-8 -*-
import cv2 
import numpy as np 
import time

start=time.perf_counter()
imagen = cv2.imread("seq/Img000100.jpg") 
imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
mask = np.zeros((imagen_gray.shape), np.uint8)
contour = np.array([[0,320],[640,320],[640,70],[0,80]])
cv2.fillPoly(mask, pts =[contour], color=(255,255,255))
masked_img = cv2.bitwise_and(mask,imagen_gray)
blur = cv2.blur(masked_img, (7,5))
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 10,param1=50,param2=20,minRadius=5,maxRadius=40)
circless = 0

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(masked_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        circless+=1
        
end=time.perf_counter()
print("En la imagen hay ",circless," celulas")
print(f"Celulas detectadas en {end - start:0.4f} segundos")

# Resultados
cv2.imshow('img', masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
