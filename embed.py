import numpy as np
import cv2
from DWT2 import *
if __name__ == '__main__':
    image = cv2.imread("index.jpeg")
    height, width= image.shape[:2]
    image2, imArray2 =waveleteTransform(image,width,height)
    image3, imArray3=inverseWaveleteTransform(imArray2,width,height)
    cv2.imshow("image",image3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def embed():
    image = cv2.imread("index.jpeg")
    height, width= image.shape[:2]
    width2 = width/2;
    for i in range(height):
        for j in range(0,width-1,2):

            j1 = j+1;
            j2 = j/2;

            result[i,j2] = (image[i,j] + image[i,j1])/2;
            result[i,width2+j2] = (image[i,j] - image[i,j1])/2;

    #copy array
    image=np.copy(result)

    # Vertical processing:
    height2 = height/2;
    for i in range(0,height-1,2):
        for j in range(0,width):

            i1 = i+1;
            i2 = i/2;

            result[i2,j] = (image[i,j] + image[i1,j])/2;
            result[height2+i2,j] = (image[i,j] - image[i1,j])/2;
    resultimg=result.astype(np.uint8)
    return resultimg ,result
