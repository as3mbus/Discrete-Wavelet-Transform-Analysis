import cv2
import numpy as np
# import sys
import math


def mse(image1, image2):
    height, width = image1.shape[:2]
    mse = np.zeros((3), np.double)
    x = np.float(1)
    # print x
    x = x / (height * width)
    # print x
    for a in range(height):
        for b in range(width):
            mse += pow((image1[a, b] - image2[a, b]), 2)
            # print str(image1[a,b]) + " - " + str(image1[a,b])
    # print mse
    mse = mse * x
    # print mse
    # print 10*np.log10(math.pow(255,2)/mse)
    return mse, 10 * np.log10(math.pow(255, 2) / mse)


def rgb2gs(rgb):
    val = 0.114 * (rgb[0]) + 0.587 * (rgb[1]) + 0.299 * (rgb[2])
    return val


if __name__ == '__main__':
    image1 = cv2.imread("/tmp/awal.jpeg")
    image2 = cv2.imread("/tmp/resultdwt.jpeg")
    MSE, PSNR = MSE(image1, image2)
    # print glcm
    print "MSE = " + str(rgb2gs(MSE))
    print "PSNR = " + str(rgb2gs(PSNR))

    cv2.imshow("testing", image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
