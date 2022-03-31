#
# AIMER: Artificial Intelligence Mark Evaluator & Recognizer
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