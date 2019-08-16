from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import imutils
from ImageUtils import ShowImage, GetContours, CropRectangleFromImage, DrawContour, BinaryInvertImage
from ShapeUtils import CheckIfCircle

print(cv.__version__)


def thresh_callback(image):
    # Convert image to gray and blur it
    src_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # src_gray = cv.blur(src_gray, (3, 3))
    # src_gray = cv.GaussianBlur(image, (5, 5), 0)
    src_gray = cv.medianBlur(src_gray, 3)
    max_thresh = 255
    _, src_gray = cv.threshold(src_gray, 127, max_thresh, cv.THRESH_OTSU)

    threshold = 50  # initial threshold

    # [findContours]
    contours, hierarchy = cv.findContours(
        src_gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # [findContours]

    # Getting semi-circles
    circles = list(filter(lambda c: CheckIfCircle(c), contours))

    # [Getting rectangles]
    contours_poly = [None]*len(contours)
    for i, c in enumerate(contours):
        closed = True
        epsilon = 0.1*cv.arcLength(c, closed)
        contours_poly[i] = cv.approxPolyDP(c, epsilon, closed)
    # [Getting rectangles]

    buffer = 2

    def checkForRectangleContour(c, img):
        minCriteria = len(c) == 4 and cv.contourArea(c) > 200.0
        if(minCriteria):
            c = list(map(lambda v: v[0], c))
            # checking for straightness
            xCheck = abs(c[2][0]-c[3][0]) <= buffer and abs(c[0]
                                                            [0]-c[1][0]) <= buffer
            yCheck = abs(c[0][1]-c[3][1]) <= buffer and abs(c[1]

                                                            [1]-c[2][1]) <= buffer
            if not (minCriteria and xCheck and yCheck):
                return False
            # Check if rectangular contour is falsely image itself
            imgDim = img.shape[:2]
            if any([any(cond) for cond in
                    ([([abs(x-y) <= buffer for x in v for y in imgDim])
                      for v in c])]):
                return False
            return True
        else:
            return False

    rectangles = list(
        filter(lambda contour: checkForRectangleContour(contour, image), contours_poly))

    # DrawContour(image, rectangles)
    rectangle = np.reshape(rectangles[0], (4, 2))
    x1 = np.min(rectangle, axis=0)[0]
    (x2, y2) = np.max(rectangle, axis=0)
    # swapping is needed to translate contours to image coordinates
    # Since coordinates are calculated from left top origin
    croppedImg = src_gray[y2:, x1:x2]
    canniedImage = cv.Canny(croppedImg, threshold, 2*threshold)
    dimension_line = list(filter(lambda cnt: len(
        cnt) > 4, GetContours(canniedImage)))[0]
    digitarea = CropRectangleFromImage(croppedImg, dimension_line)
    ShowImage(digitarea)
    return digitarea


def shapeDetection(imagePath):
    image = cv.imread(imagePath)
    return thresh_callback(image)
