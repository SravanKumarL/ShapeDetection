import cv2 as cv
import numpy as np


def DrawHoughCircle(image):
    circles = cv.HoughCircles(image=image, method=cv.HOUGH_GRADIENT, dp=1,
                              minDist=100, param1=200, param2=40, minRadius=0, maxRadius=0)

    for circle in circles[0]:
        cv.circle(image, (circle[0], circle[1]),
                  circle[2], color=(0, 255, 0), thickness=2)


def CheckIfCircle(contour, closed=True):
    epsilon = 0.005*cv.arcLength(contour, closed)
    approx = cv.approxPolyDP(contour, epsilon, closed)
    area = cv.contourArea(contour)
    return len(approx) >= 8 and len(approx) <= 10 and area > 200.0
