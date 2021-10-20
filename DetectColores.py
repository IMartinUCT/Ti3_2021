import cv2 
import cv2 
import numpy as np 
import time




circless,circuloA,circuloR = 0,0,0
image = cv2.imread('seq/Img001212.jpg')
start=time.perf_counter()

imagen_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = np.zeros((imagen_gray.shape), np.uint8)
contour = np.array([[0,185],[640,175],[640,70],[0,80]])
cv2.fillPoly(mask, pts =[contour], color=(255,255,255))
masked_img = cv2.bitwise_and(mask,imagen_gray)
blur = cv2.blur(masked_img, (7,5))

circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.05, 10,param1=20,param2=12,minRadius=7,maxRadius=12)
circles2 = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 2, 10, param1=100, param2=50, minRadius=30, maxRadius=40)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(image, (i[0], i[1]), i[2], (255, 255, 255), 1)
        circless+=1
    
if circles2 is not None: 
    circles2 = np.uint16(np.around(circles2))
    for i in circles2[0,:]:
        b,g,r = image[i[1], i[0]]
        if (b > r) :
            cv2.circle(image, (i[0], i[1]), i[2], (255,0,0), 2)
            circuloA += 1
            circless+=1
            
        elif(r > b):
            cv2.circle(image, (i[0], i[1]), i[2], (0,0,255), 2)
            circuloR += 1
            circless+=1
        else:
            cv2.circle(image, (i[0], i[1]), i[2], (255, 255, 255), 2)
            circless+=1

end=time.perf_counter()
print("En la imagen hay ",circless," celulas")
print(f"Celulas detectadas en {end - start:0.4f} segundos")
print("Celulas Rojas = ",circuloR)
print("Celulas Azules = ",circuloA)
cv2.imshow('img', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
