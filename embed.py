import numpy as np
import cv2
def embed(imArray,imWater,x,y,w,h):
    waterHeight,waterWidth=imWater.shape[:2]
    if w<waterWidth or h<waterHeight:
        if waterHeight>waterWidth:
            print waterHeight/h
            imWater = cv2.resize(imWater,(0,0), fx=float(h/waterHeight), fy=float(h/waterHeight))
        else :
            print  str(w) + "/" + str(waterWidth) +" = "+ str(float(w)/waterWidth)
            imWater = cv2.resize(imWater,(0,0), fx = float(w)/waterWidth, fy = float(w)/waterWidth)

        waterHeight,waterWidth=imWater.shape[:2]
        crop_imArray = imArray[y:waterHeight+y,x:waterWidth+x]
        resultWater = (0.5*crop_imArray) + (0.5 *imWater)
        imArray[y:waterHeight+y,x:waterWidth+x]=resultWater
    else :
        crop_imArray = imArray[y:waterHeight+y,x:waterWidth+x]
        resultWater = (0.5*crop_imArray) + (0.5 * imWater)
        imArray[y:waterHeight+y,x:waterWidth+x]=resultWater
    resultImgWater=resultWater.astype(np.uint8)
    resultImgArray=imArray.astype(np.uint8)

    cv2.imshow("crop",crop_imArray)
    cv2.imshow("tesss", resultImgWater)
    cv2.imshow("aaaaa", resultImgArray)
    cv2.waitKey(0)
    return resultImgWater ,resultWater

if __name__ == '__main__':
        image = cv2.imread("/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/Picture1.png")
        imageWater = cv2.imread("/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/gambar.jpg")
        height, width= image.shape[:2]
        print "A"
        # imWater = cv2.resize(imageWater,(0,0), fx = float(height/200), fy = float(height/200))
        resultWater, resultImgWater = embed(image,imageWater,100,0,50,120)
        # cv2.imshow("ori", imageWater)
        # cv2.imshow("resiz", imWater)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
