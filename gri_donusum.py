import cv2
import numpy

def convertGray(image):
    resultImage=numpy.zeros((image.shape[0],image.shape[1],1),dtype=numpy.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            resultImage[i,j]=image[i,j,0]*0.299+image[i,j,1]*0.587+image[i,j,2]*0.114
    return resultImage

image=cv2.imread(r"C:\Users\yunusemrecoskun\Desktop\cat.jpg")
grayImage=convertGray(image)
cv2.imshow("Gray Image",grayImage)
cv2.waitKey(0)
