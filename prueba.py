# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 17:24:32 2021

@author: Bryan
"""
import cv2
import os
import numpy as np

contenido = os.listdir('Seq') #listamos el directorio y lo guardamos en la variable contenido
#print("hay ",len(contenido)," imagenes en total")
#print(contenido[0])

image1 = cv2.imread("Seq/"+str(contenido[0]))

img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
_, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2);
#th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2);

gauss = cv2.GaussianBlur(th2, (15,15), 1)
ctns, _ = cv2.findContours(gauss, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, ctns, -1, (0,0,255), 1) #contorno 

#cv2.imshow('Imagen Bordes', bordes) 
cv2.imshow('Imagen Original', img) 

cv2.imshow("THRESH_BINARY", th1)
cv2.imshow("ADAPTIVE_THRESH_MEAN_C", th2)
#cv2.imshow("ADAPTIVE_THRESH_GAUSSIAN_C", th3)

cv2.waitKey(0)
cv2.destroyAllWindows()