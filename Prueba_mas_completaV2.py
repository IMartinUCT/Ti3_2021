# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 03:19:39 2021

@author: Bryan
"""
"""
este codigo esta cerrando lascelulas pequeñas y grandes, se puede probar con las siguientes imagenes a modo de
ejemplo...04-54... la 1010 tiene muchas celulas y borrosas, no se cuentan bien
"""
import cv2 
import numpy as np 

#leemos la imagen en escala de grises, ese parametro es un flag y tambien se puede utilizar 0 para representar GRAYSCALE
cr = cv2.imread("seq/Img000423.jpg",cv2.IMREAD_GRAYSCALE) 
#devolvemos un array llena de 0, le pasamos la forma con un shape a cr y el data-type que sera uint8
mask = np.zeros((cr.shape), np.uint8)
#creamos una matriz con valores para pintar arriba
contour = np.array([[0,320],[640,320],[640,70],[0,80]])

#con la funcion fillpoly pintamos arriba, lo que hacemos es pasarle los vertices de la imagen que queremos pintar
cv2.fillPoly(mask, pts =[contour], color=(255,255,255))

masked_img = cv2.bitwise_and(mask,cr)
blur = cv2.blur(masked_img, (7,5), 0)
_,th = cv2.threshold(blur,10,10,cv2.THRESH_BINARY)


circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 10,param1=50,param2=20,minRadius=5,maxRadius=40)

cc = 0
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        #dibujamos contorno 
        cv2.circle(masked_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        #dibujamos centro
        cv2.circle(masked_img,(i[0],i[1]),2,(255,255,255),-1)
        cc+=1
print("En la imagen hay ",cc," celulas")
# Show result for testing:
cv2.imshow('img', masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()