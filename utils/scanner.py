#
# This file is part of AIMER.
# Unpublished Copyright (C) 2022  Fereydoun Memarzanjany ("AUTHOR"), All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of AUTHOR.  The intellectual and technical concepts contained herein are 
# proprietary to AUTHOR and may be covered by U.S. and Foreign Patents, patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from AUTHOR.
# Access to the source code contained herein is hereby forbidden to anyone except current AUTHOR employees, managers or contractors who have executed 
# Confidentiality and Non-disclosure agreements explicitly covering such access.
#
# The copyright notice above does not evidence any actual or intended publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of AUTHOR.  ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE, 
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF AUTHOR IS STRICTLY PROHIBITED, AND IN VIOLATION OF 
# APPLICABLE LAWS AND INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY 
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
#

import cv2 as cv
import numpy as np


# Sorts a given list of points in a clock-wise manner.
def sort_points(points):
    points = np.reshape(points, (4, 2)) # FOUR pairs of (x, y) coordinates
    sorted_points = np.zeros((4, 2), dtype=np.int32)

    summation = np.sum(points, axis=1)
    sorted_points[0] = points[np.argmin(summation)]
    sorted_points[3] = points[np.argmax(summation)]

    difference = np.diff(points, axis=1)
    sorted_points[1] = points[np.argmin(difference)]
    sorted_points[2] = points[np.argmax(difference)]

    return sorted_points

# Usually, the paper or document in an image, when compared with other objects (e.g., pens, erasers, etc), would be the largest shape.
def find_largest_contours(contours):
    largest = np.array([])

    max_area = 0 # A variable to hold the highest area of each contour and check it against the next contour.
    
    for contour in contours:
        area = cv.contourArea(contour)

        if area > 5000:
            # True in these two lines indicates that the "curve" (shape) is a closed one (rectangle in this case).
            perimeter = cv.arcLength(contour, True)
            curve = cv.approxPolyDP(contour, (0.02*perimeter), True)

            if (area > max_area) and (len(curve) == 4): # Rectangles have 4 points.
                max_area = area
                largest = curve

    return largest

# TODO: Move these to a centralized configuration section or file.
#
# 480p for a higher processing speed
WIDTH = 640
HEIGHT = 480
# The margin or outline/border of the document
MARGIN = 25 # TODO: Obtain this automatically from the image dimensions and ratios.

def scan(img):
    img = cv.resize(img, (WIDTH, HEIGHT))
    img_original = img

    img_grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_grayscale = cv.GaussianBlur(img_grayscale, (5, 5), 1)

    img_grayscale = img

    # TODO: lower the brightness and preserve edges.
    #img = cv.bilateralFilter(img, 11, 17, 17)
    img = cv.Canny(img, 200, 200)

    kernel = np.ones((5, 5))
    img = cv.dilate(img, kernel, iterations=2)
    img = cv.erode(img, kernel, iterations=1)

    #cv.namedWindow("debug")
    #cv.imshow("debug", img)


    # Extracts all the shapes ("contours") from the image.
    contours, _hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    largest_countors = find_largest_contours(contours) # Finds the largest contour.
    if largest_countors.size == 0: # No shapes were detected.
        return img_original, np.zeros((HEIGHT, WIDTH, 3), np.uint8) # So, we return a blank image.
    
    img_bordered = img_original
    cv.drawContours(img_bordered, [largest_countors.astype(int)], -1, (0, 255, 0), 2)

    largest_countors = sort_points(largest_countors) # Sorts its points.

    # De-skew the image
    src = np.float32(largest_countors) # Coordinates of the largest shape (i.e., the paper or document).
    dst = np.float32([[0, 0], [WIDTH, 0], [0, HEIGHT], [WIDTH, HEIGHT]]) # Same size as the resized img.
    matrix = cv.getPerspectiveTransform(src, dst)
    img_scanned = cv.warpPerspective(img_original, matrix, (WIDTH, HEIGHT))


    # Crops the blurry outline/margin.
    img_scanned = img_scanned[MARGIN:img_scanned.shape[0]-MARGIN, MARGIN:img_scanned.shape[1]-MARGIN]
    img_scanned = cv.resize(img_scanned, (WIDTH, HEIGHT))

    # Anti-aliasing
    img_scanned = cv.medianBlur(img_scanned, 9)

    return img_bordered, img_scanned