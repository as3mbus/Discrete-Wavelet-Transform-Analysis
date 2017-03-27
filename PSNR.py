import cv2
import numpy as np
# import sys
import math

def MSE(image1,image2):
    height, width= image1.shape[:2]
    mse = np.zeros((3), np.double)
    x = np.float(1)
    # print x
    x = x/(height*width)
    print x
    for a in range(height):
        for b in range(width):
            mse += pow((image1[a,b]-image2[a,b]),2)
            # print str(image1[a,b]) + " - " + str(image1[a,b])
    print mse
    mse = mse*x
    print mse
    return mse;


if __name__ == '__main__':
    image1=cv2.imread("index.jpeg")
    image2=cv2.imread("indexD.jpeg")
    MSE(image1,image2)
    # print glcm

    cv2.imshow("testing",image1)
    cv2.imwrite("a.jpeg",image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
