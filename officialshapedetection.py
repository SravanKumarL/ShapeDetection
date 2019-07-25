from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import random as rng
import imutils

print(cv.__version__)
rng.seed(12345)


def thresh_callback(val):
    threshold = val

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
    copy = src.copy()
    index = 10
    # contours=map(lambda:c:cv.approxPolyDP())
    rectContours = list(filter(lambda c: len(c) <= 5, contours))
    cv.drawContours(copy, rectContours, -1, (0, 255, 0), 1)
    windName = 'Contours'
    cv.namedWindow(windName, cv.WINDOW_NORMAL)
    cv.resizeWindow(windName, 600, 600)
    cv.imshow(windName, copy)
    return

    # [allthework]
    # Approximate contours to polygons + get bounding rects and circles
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        closed = True
        epsilon = cv.arcLength(c, closed)*0.04
        contours_poly[i] = cv.approxPolyDP(c, epsilon, closed)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    # [allthework]

    # [zeroMat]
    drawing = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    # [zeroMat]

    # [forContour]
    # Draw polygonal contour + bonding rects + circles
    for i in range(len(contours)):
        # color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        color = (0, 255, 0)
        cv.drawContours(copy, contours_poly, i, color, 1)
        # cv.rectangle(copy, (int(boundRect[i][0]), int(boundRect[i][1])),
        #              (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 1)
        # cv.circle(copy, (int(centers[i][0]), int(
        #     centers[i][1])), int(radius[i]), color, 2)
    # [forContour]

    # [showDrawings]
    # Show in a window
    cv.imshow('Contours', copy)
    # [showDrawings]


# [setup]
# Load source image
parser = argparse.ArgumentParser(
    description='Code for Creating Bounding boxes and circles for contours tutorial.')
parser.add_argument('--image', help='Path to input image.',
                    default='stuff.jpg')
args = parser.parse_args()

# src = cv.imread(cv.samples.findFile(args.input))
src = cv.imread(args.image)
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)

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
thresh_callback(thresh)
# [trackbar]

cv.waitKey()
