import cv2
import numpy as np
# import sys
import math


def GLCM(image, height ,width , dy,dx):
    glcm=np.zeros((256,256,3),np.double)
    x=0
    for i in range(height):
        for j in range(width):
            if i+dy in range(height) and j+dx in range(width):
                glcm[image[i,j,0],image[i+dy,j+dx,0],0] +=1
                glcm[image[i,j,1],image[i+dy,j+dx,1],1] +=1
                glcm[image[i,j,2],image[i+dy,j+dx,2],2] +=1
                # print str(image[i,j,0]) + " " + str(image[i+dy,j+dx,0]) + "  " + str(glcm[image[i,j,0],image[i+dy,j+dx,0],0])
                x+=1
    glcm=glcm/x
    return glcm

def contrast(glcm):
    contrast=np.zeros(3,np.float)
    meanI = np.zeros(3, np.float)
    meanJ = np.zeros(3, np.float)
    energy = np.zeros(3,np.float)
    homogenity = np.zeros(3,np.float)
    for i in range(256):
        for j in range(256):
            contrast[0]+=pow(i-j,2)*glcm[i,j,0]
            contrast[1]+=pow(i-j,2)*glcm[i,j,1]
            contrast[2]+=pow(i-j,2)*glcm[i,j,2]
            meanI[0]+=i*glcm[i,j,0]
            meanI[1]+=i*glcm[i,j,1]
            meanI[2]+=i*glcm[i,j,2]
            meanJ[0]+=j*glcm[i,j,0]
            meanJ[1]+=j*glcm[i,j,1]
            meanJ[2]+=j*glcm[i,j,2]
            energy[0]+=pow(glcm[i,j,0],2)
            energy[1]+=pow(glcm[i,j,1],2)
            energy[2]+=pow(glcm[i,j,2],2)
            homogenity[0]+=glcm[i,j,0] / (1+ abs(i-j))
            homogenity[1]+=glcm[i,j,1] / (1+ abs(i-j))
            homogenity[2]+=glcm[i,j,2] / (1+ abs(i-j))
    return contrast, meanI, meanJ ,energy, homogenity

def correlation(glcm, meanI, meanJ,taoI, taoJ):
    correlation=np.zeros(3,np.float)
    for i in range(256):
        for j in range(256):
            correlation[0]+=((i-meanI[0]) * (j-meanJ[0])* glcm[i,j,0]) / (taoI[0]*taoJ[0])
            correlation[1]+=((i-meanI[1]) * (j-meanJ[1]) * glcm[i,j,1]) / (taoI[1]*taoJ[1])
            correlation[2]+=((i-meanI[2]) * (j-meanJ[2]) * glcm[i,j,2]) / (taoI[2]*taoJ[2])
            # print correlation;
    return correlation


def tao(glcm,meanI,meanJ):
    taoI=np.zeros(3, np.float)
    taoJ=np.zeros(3, np.float)
    for i in range(256):
        for j in range(256):
            taoI[0]=pow(i-meanI[0],2) * glcm[i,j,0]
            taoI[1]=pow(i-meanI[1],2) * glcm[i,j,1]
            taoI[2]=pow(i-meanI[2],2) * glcm[i,j,2]
            taoJ[0]=pow(j-meanJ[0],2) * glcm[i,j,0]
            taoJ[1]=pow(j-meanJ[1],2) * glcm[i,j,1]
            taoJ[2]=pow(j-meanJ[2],2) * glcm[i,j,2]
            # print str(pow(j-meanJ[1],2)) + " x " + str(glcm[i,j,1])
    # print "taoi = "
    # print taoI
    # print "taoj = "
    # print taoJ
    for i in range(3):
        taoI[i]=math.sqrt(taoI[i])
        taoJ[i]=math.sqrt(taoJ[i])
    return taoI, taoJ

if __name__ == '__main__':
    image=cv2.imread("tes.jpeg")
    height,width = image.shape[:2]
    glcm=GLCM(image,height,width,0,1)
    imglcm=glcm.astype(np.uint8)
    kontras, meanI, meanJ, energy, homogenity=contrast(glcm)
    taoI, taoJ=tao(glcm,meanI,meanJ)
    korelasion=correlation(glcm,meanI,meanJ,taoI,taoJ)
    print "meanI = " + str(meanI)
    print "meanJ = " + str(meanJ)
    print "taoI = " + str(taoI)
    print "taoJ = " + str(taoJ)
    print "kontras = " +  str(kontras)
    print "Energy = " +  str(energy)
    print "Homogenitas = " +  str(homogenity)
    print "Correlation = " + str(korelasion)
    # print glcm

    cv2.imshow("testing",imglcm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


