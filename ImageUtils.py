import cv2
import imutils
import numpy as np


def ShowImage(image, width=None, height=None):
    isDimSpecified = width is not None and height is not None
    cv2.namedWindow(
        'IMAGE', cv2.WINDOW_NORMAL if isDimSpecified else cv2.WINDOW_AUTOSIZE)
    if isDimSpecified:
        cv2.resizeWindow('IMAGE', width=width, height=height)
    cv2.imshow('IMAGE', image)
    cv2.waitKey(0)


def GetContours(image, SORT=True):
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if(SORT):
        cnts = imutils.contours.sort_contours(cnts,
                                              method="left-to-right")[0]
    return cnts


def DrawContour(image, contours=None, cntrIdx=-1, thickness=2):
    if contours is None:
        contours = GetContours(image, True)
    cv2.drawContours(image, contours, cntrIdx,
                     (0, 255, 0), thickness=thickness)
    ShowImage(image)
    return


def CropRectangleFromImage(image, rectangle, buffer=4):
    (x, y) = np.max(rectangle, axis=0)[0]
    return image.copy()[:y-buffer, :]


def BinaryInvertImage(image, thresh=127):
    return cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY_INV)[1]
