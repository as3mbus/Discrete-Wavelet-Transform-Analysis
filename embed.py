import numpy as np
import cv2
# def embed(imArray,imWater,x,y,w,h):
#     waterHeight,waterWidth=imWater.shape[:2]
#     if w<waterWidth or h<waterHeight:
#         if waterHeight>waterWidth:
#             print waterHeight/h
#             imWater = cv2.resize(imWater,(0,0), fx=float(h/waterHeight), fy=float(h/waterHeight))
#         else :
#             # print  str(w) + "/" + str(waterWidth) +" = "+ str(float(w)/waterWidth)
#             imWater = cv2.resize(imWater,(0,0), fx = float(w)/waterWidth, fy = float(w)/waterWidth)
#
#         waterHeight,waterWidth=imWater.shape[:2]
#         crop_imArray = imArray[y:waterHeight+y,x:waterWidth+x]
#         resultWater = (0.8*crop_imArray) + (0.2 *imWater)
#         imArray[y:waterHeight+y,x:waterWidth+x]=resultWater
#     else :
#         crop_imArray = imArray[y:waterHeight+y,x:waterWidth+x]
#         resultWater = (0.8*crop_imArray) + (0.2 * imWater)
#         imArray[y:waterHeight+y,x:waterWidth+x]=resultWater
#     resultImgWater=resultWater.astype(np.uint8)
#     resultImgArray=imArray.astype(np.uint8)
#
#     cv2.waitKey(0)
#     return resultImgArray


def embed(imArray, imWater, x, y, w, h, alpha):
    imArray = imArray.astype(np.float)
    imWater = imWater.astype(np.float)
    waterHeight, waterWidth = imWater.shape[:2]
    if w < waterWidth or h < waterHeight:
        if waterHeight > waterWidth:
            print waterHeight / h
            imWater = cv2.resize(imWater, (0, 0), fx=float(
                h / waterHeight), fy=float(h / waterHeight))
        else:
            # print  str(w) + "/" + str(waterWidth) +" = "+
            # str(float(w)/waterWidth)
            imWater = cv2.resize(imWater, (0, 0), fx=float(
                w) / waterWidth, fy=float(w) / waterWidth)

        waterHeight, waterWidth = imWater.shape[:2]
        crop_imArray = imArray[y:waterHeight + y, x:waterWidth + x]
        resultWater = crop_imArray.astype(
            np.float) + alpha * imWater.astype(np.float)
        imArray[y:waterHeight + y, x:waterWidth + x] = resultWater
    else:
        crop_imArray = imArray[y:waterHeight + y, x:waterWidth + x]
        resultWater = crop_imArray.astype(
            np.float) + alpha * imWater.astype(np.float)
        imArray[y:waterHeight + y, x:waterWidth + x] = resultWater
    resultImgWater = resultWater.astype(np.uint8)
    resultImgArray = imArray.astype(np.uint8)
    imArray = imArray.astype(np.uint8)
    imWater = imWater.astype(np.uint8)
    return resultImgArray

def extract(img, imgcover, alpha):

    watermark = ((img.astype(np.double) -
                  imgcover.astype(np.double)) / alpha).astype(np.uint8)
    return watermark

if __name__ == '__main__':
    image = cv2.imread(
        "/home/as3mbus/Screenshot_2017-04-09_22-30-51.png")
    imageWater = cv2.imread(
        "/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/tes.jpeg")
    height, width = image.shape[:2]
    print "A"
    # imWater = cv2.resize(imageWater,(0,0), fx = float(height/200), fy = float(height/200))
    resultWater = embed(image, imageWater, 0, 0, 500, 500,0.5)
    # cv2.imshow("ori", imageWater)
    cv2.imshow("resiz", resultWater)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
