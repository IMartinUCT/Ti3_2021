#Import the necessary modules
import stapi as st #Spica exclusive module
import cv2 as cv 
import numpy as np

#Define all functions#
#Image processing and masking, returns the image with the blur filter applied and the mask necessary

def Processing(img,d1,d2):
    imagen_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)         #Img original BGR to gray scale with cvtColor function
    mask = np.zeros((imagen_gray.shape), np.uint8)            #Numpy array of zeros                  
    contour = np.array([[0,185],[640,175],[640,70],[0,80]])   #Mask to hide unwanted spots
    cv.fillPoly(mask, pts =[contour], color=(255,255,255))    #The mask is fixed with fillpoly function
    masked_img = cv.bitwise_and(mask,imagen_gray)             #The images are combined with a logical operation (AND)
    blur = cv.blur(masked_img, (7,5))                         #Blur is applied to the image with the desired parameters
    Cells(blur,d1,d2)

#Use HoughCircles for the detection of cells, returns detected cells according to size  
def Cells(blur,d1,d2):
    #We apply the necessary values for each type of cells to detect
    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, d1["dp"], d1["minDist"],param1=d1["param1"],param2=d1["param2"],minRadius=d1["minRadius"],maxRadius=d1["maxRadius"])
    circles2 = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, d2["dp"], d2["minDist"],param1=d2["param1"],param2=d2["param2"],minRadius=d2["minRadius"],maxRadius=d2["maxRadius"])
    Circles(circles, circles2)

#Function to detect cells according to their type and send them to the spica app  
def Circles(circles,circles2):
    count,count2,count3 = 0,0,0                                            #Counters for detection
    gray = np.empty([1,3],dtype = np.float32)                              #Numpy Array for packaging the data to be sent for cells gray
    blue = np.empty([1,3],dtype = np.float32)                              #Numpy Array for packaging the data to be sent for cells blue
    red = np.empty([1,3],dtype = np.float32)                               #Numpy Array for packaging the data to be sent for cells red
    
    if circles is not None:                                                #If the HoughCircles function detected cells
        circles = np.uint16(np.around(circles))                            #Numpy Array for the cells detected, 16bit image format
        for i in circles[0,:]:                                             #We go through the array
            gray_aux = np.array([[i[0],i[1],i[2]]], dtype = np.float32)    #We define an auxiliary variable for the detected cells
            if count == 0:                                                 #If the counter is empty, we occupy the auxiliary variable
                gray = gray_aux     
            else:                                                          #Otherwise we pack the detected cell to send it
                gray = np.append(gray,gray_aux,axis = 0)
            count +=1                                                      #Add 1 to the counter of gray cells

    if count > 0:                                                          #If the counter is not empty
    	st.data("gray",gray)                                               #We send the information to the Spica app with the st.data function

    if circles2 is not None:                                               #If the HoughCircles function detected cells
        circles2 = np.uint16(np.around(circles2))                          #Numpy Array for the cells detected, 16bit image format
        for i in circles2[0,:]:                                            #We go through the array
            b,g,r = img[i[1], i[0]]                                        #We have the bgr of the image
            blue_aux = np.array([[i[0],i[1],i[2]]], dtype = np.float32)    #We define an auxiliary variable for blue cells
            red_aux = np.array([[i[0],i[1],i[2]]], dtype = np.float32)     #We define an auxiliary variable for red cells
            if b > r :                                                     #If the b channel of the centroid is higher than r then the cell is blue
                if count2==0:                                              #If the counter is empty, we occupy the auxiliary variable
            	    blue=blue_aux
                else:                                                      #Otherwise we pack the detected cell to send it
                    blue = np.append(blue,blue_aux,axis = 0)
                count2+=1                                                  #Add 1 to the counter of blue cells
            elif r > b:                                                    #If the r channel of the centroid is higher than b then the cell is blue
                if count3==0:                                              #If the counter is empty, we occupy the auxiliary variable
                    red=red_aux
                else:
                    red = np.append(red,red_aux,axis = 0)                  #Otherwise we pack the detected cell to send it
                count3+=1                                                  #Add 1 to the counter of red cells

    if count2 > 0:                                                         #If the blue and red cell counters are not empty
    	st.data("blue",blue)                                               #We send the information to the Spica app with the st.data function
    if count3 > 0:	
    	st.data("red",red)
        


#Main function
if __name__ == "__main__":
    #Use of dictionaries for each value of the function Cells
    d1 = {"dp":1.05,"minDist":10,"param1":20,"param2":12,"minRadius":7,"maxRadius":12}   #Data for small circles
    d2 = {"dp":2,"minDist":10,"param1":50,"param2":50,"minRadius":30,"maxRadius":40}     #Data for big circles
    img=st.value("image")                                                                #Open the image 
    Processing(img,d1,d2)                                                                #Call the function to process the image