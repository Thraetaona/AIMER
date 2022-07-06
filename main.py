# AIMER: Artificial Intelligence Mark Evaluator & Recognizer
# Copyright (C) 2022  Fereydoun Memarzanjany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import time
from utils import camera_driver, scanner, grader
import cv2 as cv
import numpy as np

# This sets the root logger to write to stdout.  Also, by default the
# logger is set to print (only) WARNINGs, we want INFOs to get printed as well.
logging.basicConfig(encoding="utf-8", level=logging.NOTSET)

cap = camera_driver.init_camera()


def main():
    cv.namedWindow("webcam")
    cv.namedWindow("graded")

    img = None
    scanned = None

    #image = cv.imread("test.png", cv.IMREAD_GRAYSCALE)

    while True:
        _ret, img = cap.read()

        img, scanned_img = scanner.scan(img)
        cv.imshow("webscam", img)

        score, graded_img = grader.grade(scanned_img)
        cv.imshow("graded", graded_img)

        if (cv.waitKey(33) == ord('s')):
            break
        
    print("The final grade was: " + str(score) + "%")

cv.destroyAllWindows()

# Main harness function for driving the code.
if (__name__ == "__main__"): # The module is being run directly
    main()
else: # The module is being imported into another one
    pass
