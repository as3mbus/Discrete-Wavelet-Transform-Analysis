from DWT2 import *
from embed import *




if __name__ == '__main__':
    imgOriginal = cv2.imread(
        "/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/Picture1.png")
    imgOriginalDWT = waveleteTransform(imgOriginal)
    height, width = imgOriginal.shape[:2]
    imgWatermark = cv2.imread(
        "/media/DATA/UDINUS/SMT 6/Advanced Image Processing/Project/tes.jpeg")
    # imgWatermark = cv2.resize(imgWatermark, (width, height))
    # imgWatermarkDWT = waveleteTransform(imgWatermark)
    # imgWatermarkDWTLL = imgWatermarkDWT[0:height / 2, 0:width / 2]
    alpha = 0.004
    imgWatermarkedDWT = embed(
        imgOriginalDWT, imgWatermark, 0, 0, width / 2, height / 2, alpha)
    imgWatermarked = inverseWaveleteTransform(imgWatermarkedDWT)
    imgWatermarkedDDWT = waveleteTransform(imgWatermarked)
    watermark = extract(imgWatermarkedDDWT[0:height / 2, 0:width / 2],
                        imgOriginalDWT[0:height / 2, 0:width / 2], alpha)
    cv2.imshow("Original", imgOriginal)
    # cv2.imshow("OriginalDWT",imgOriginalDWT)
    cv2.imshow("Watermark", imgWatermark)
    # cv2.imshow("WatermarkDWT",imgWatermarkDWT)
    # cv2.imshow("WatermarkedDWT",imgWatermarkedDWT)
    cv2.imshow("Watermarked", imgWatermarked)
    # cv2.imshow("Watermarked2",imgWatermarkedDDWT)
    cv2.imshow("extract", watermark)

    cv2.waitKey(0)
