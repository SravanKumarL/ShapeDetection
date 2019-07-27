from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import imutils

print(cv.__version__)


def thresh_callback(threshold, src_gray):
    # [Canny]
    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    # [Canny]

    # [findContours]
    # Find contours
    contours, hierarchy = cv.findContours(
        canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # [findContours]

    # testcode
    # copy = src.copy()
    # index = 1

    # def getApproxPoly(c):
    #     epsilon = 0.1*cv.arcLength(c, True)
    #     return cv.approxPolyDP(c, epsilon, True)
    # contours = list(map(lambda c: getApproxPoly(c), contours))
    # rectContours = list(filter(lambda c: len(c) <= 5, contours))
    # cv.drawContours(copy, rectContours, -1, (0, 255, 0), 1)
    # windName = 'Contours'
    # cv.namedWindow(windName, cv.WINDOW_NORMAL)
    # cv.resizeWindow(windName, 600, 600)
    # cv.imshow(windName, copy)
    # return

    # [allthework]
    # Approximate contours to polygons + get bounding rects and circles
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    # centers = [None]*len(contours)
    # radius = [None]*len(contours)
    # minRect = [None]*len(contours)
    # minEllipse = [None]*len(contours)

    for i, c in enumerate(contours):
        closed = True
        epsilon = 0.04*cv.arcLength(c, closed)
        contours_poly[i] = cv.approxPolyDP(c, epsilon, closed)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        # centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
        # minRect[i] = cv.minAreaRect(c)
        # if c.shape[0] > 5:
        #     minEllipse[i] = cv.fitEllipse(c)
    # [allthework]

    # [zeroMat]
    drawing = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    # [zeroMat]

    # [forContour]
    # Draw polygonal contour + bounding rects + circles
    def checkForRectangleContour(c):
        minCriteria = len(c) == 4 and cv.contourArea(c) > 100
        return minCriteria
    contours_poly = list(
        filter(lambda contour: checkForRectangleContour(contour), contours_poly))
    color = (0, 255, 0)

    # cv.drawContours(drawing,  minEllipse, 5, color, 1)
    # for i, c in enumerate(contours):
    cv.drawContours(src_gray,  contours_poly, 4, color, 1)
    # if c.shape[0] > 5 and (minEllipse[i] is not None):
    #     minEllipse[i] = (minEllipse[i][0], tuple(i/2 for i in minEllipse[i][1]),
    #                      minEllipse[i][2])
    #     cv.ellipse(copy, minEllipse[i], color, 2)
    # cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),
    #              (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 1)
    # cv.circle(src_gray, (int(centers[i][0]), int(
    #     centers[i][1])), int(radius[i]), color, 2)
    # [forContour]

    # [showDrawings]
    # Show in a window
    cv.imshow('Contours', src_gray)
    cv.waitKey(0)
    # return contours_poly
    # [showDrawings]


# [setup]
# Load source image
# parser = argparse.ArgumentParser(
#     description='Code for Creating Bounding boxes and circles for contours tutorial.')
# parser.add_argument('--image', help='Path to input image.',
#                     default='stuff.jpg')
# args = parser.parse_args()

# src = cv.imread(cv.samples.findFile(args.input))
def shapeDetection(image):
    src = cv.imread(image)

    # Convert image to gray and blur it
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    src_gray = cv.blur(src_gray, (3, 3))
    # [setup]

    # [createWindow]
    # Create Window
    # source_window = 'Source'
    # cv.namedWindow(source_window)
    # cv.imshow(source_window, src)
    # [createWindow]
    # [trackbar]
    max_thresh = 255
    thresh = 100  # initial threshold
    # cv.createTrackbar('Canny thresh:', source_window,
    #                   thresh, max_thresh, thresh_callback)
    return thresh_callback(thresh, src_gray)
    # [trackbar]
