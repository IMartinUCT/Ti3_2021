# -*- coding: utf-8 -*-
import cv2 
import numpy as np 
import time

start=time.perf_counter()
imagen = cv2.imread("seq/Img000041.jpg") 
imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
mask = np.zeros((imagen_gray.shape), np.uint8)
contour = np.array([[0,185],[640,175],[640,70],[0,80]])

cv2.fillPoly(mask, pts =[contour], color=(255,255,255))
masked_img = cv2.bitwise_and(mask,imagen_gray)
blur = cv2.blur(masked_img, (7,5))
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDist=10,param1=50,param2=20,minRadius=5,maxRadius=40)
circless = 0

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(masked_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        circless+=1
        
#Abrimos la imagen en HSV (Hue, Saturation, value)
imagenhsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

#definimos un umbral del azul mas bajo y alto que debe encontrar
Ab = np.array([110, 50, 50], np.uint8)
Aa = np.array([130, 255, 225], np.uint8)
#Lo mismo para el color rojo
Rb = np.array([160, 50, 20], np.uint8)
Ra = np.array([180, 255, 255], np.uint8)

#Usamos estos umbrales como mascaras para transformar las imagenes a binario
#donde solo se deberian ver de color blanco los valores seleccionados
maskA = cv2.inRange(imagenhsv, Ab, Aa)
cv2.imshow('Celulas azules', maskA)
maskR = cv2.inRange(imagenhsv, Rb, Ra)
cv2.imshow('Celulas rojas', maskR)

#usando las imagenes producidas anteriormente encontrmos circulos un poco mas
#grandes de lo normal puesto que los de color siempre son mas grandes
circlesA = cv2.HoughCircles(maskA, cv2.HOUGH_GRADIENT, 1, minDist=10,param1=50,param2=20,minRadius=15,maxRadius=40)
circuloA = 0
if circlesA is not None:
    circlesA = np.uint16(np.around(circlesA))
    for i in circlesA[0,:]:
        cv2.circle(imagen, (i[0], i[1]), i[2], (255, 0, 0), 2)#Dibujamos el circulo en la imagen a color
        circuloA+=1
#Hacemos los mismo para las de color rojo        
circlesR = cv2.HoughCircles(maskR, cv2.HOUGH_GRADIENT, 1, minDist=10,param1=50,param2=20,minRadius=15,maxRadius=40)
circuloR = 0
if circlesR is not None:
    circlesR = np.uint16(np.around(circlesR))
    for i in circlesR[0,:]:
        cv2.circle(imagen, (i[0], i[1]), i[2], (0, 0, 255), 2)#Dibujamos el circulo en la imagen a color
        circuloR+=1
        
end = time.perf_counter()
print("En la imagen hay ",circless," celulas")
print(f"Celulas detectadas en {end - start:0.4f} segundos")
#Mostramos el resultado
print("He encontrado {} celulas azules".format(circuloA))
print("He encontrado {} celulas rojas".format(circuloR))

# Resultados
cv2.imshow('colores', imagen)
cv2.imshow('img', masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()