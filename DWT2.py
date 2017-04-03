import numpy as np
import cv2
import sys
import os


if __name__ == '__main__':

    #loadImage & copy image
    image = cv2.imread(sys.argv[1])
    height, width= image.shape[:2]

    image2, imArray2 =waveleteTransform(image,width,height)

    image3, imArray3=inverseWaveleteTransform(imArray2,width,height)

    cv2.imshow('base Image',image)
    cv2.imshow('DWT',image2)
    cv2.imshow('result4',image3)

    a,ext=os.path.splitext(os.path.basename(sys.argv[1]))
    a=a+"D"
    print a
    b=a+ext
    print b
    cv2.imwrite('/tmp/image3.jpeg',image3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def waveleteTransform(img,width,height):
    # print(img)
    image=img.astype(np.int)
    result = np.zeros((height,width,3), np.int)

    #Horizontal processing
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


def inverseWaveleteTransform(img,nc,nr):
    image=img.astype(np.int)
    result=np.zeros((nr,nc,3), np.int)
    nr2 = nr/2;

    for i in range(0,nr-1,2):
        for j in range(0,nc):

            i1 = i+1
            i2 = i/2

            result[i,j] = ((image[i2,j]/2) + (image[nr2+i2,j]/2))*2;
            result[i1,j] = ((image[i2,j]/2) - (image[nr2+i2,j]/2))*2;

    # //copy array
    image=np.copy(result)

    # // Horizontal processing:
    nc2 = nc/2;
    for i in range(0,nr) :
        for j in range(0,nc-1,2):

            j1 = j+1;
            j2 = j/2;
            result[i,j] = ((image[i,j2]/2) + (image[i,j2+nc2]/2))*2;
            result[i,j1] =((image[i,j2]/2) - (image[i,j2+nc2]/2))*2;

    resultimg=result.astype(np.uint8)
    return resultimg, result;
