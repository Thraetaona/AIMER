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

import logging
import time
import cv2 as cv

# TODO: Move these to a centralized configuration section or file.
#
CAMERA_SOURCE = int(0) # 0 is the default camera device.
# Most cameras are at least 720p (1280x720 pixels) and have a frame rate of 30hz.
CAMERA_WIDTH = float(1280)
CAMERA_HEIGHT = float(720)
CAMERA_FPS = float(30)
VIDEO_BACKEND = cv.CAP_DSHOW # TODO: Directshow video backend is not portable outside of Windows.
# The string below is case insensitive
VIDEO_CODEC = "mjpg" # MJPG is widely supported, even though H.265 is better.


# Initializes a camera video stream and configures it for the best possible performance.
#
# TODO: The school does not allow class interfaces, despite being suited better for this camera driver.  Use them later individually.
def init_camera():
    logging.info("Attempting to open the default camera device at index `" + str(CAMERA_SOURCE) + "`...")
    # Captures a video stream.
    cap = cv.VideoCapture(CAMERA_SOURCE, VIDEO_BACKEND)
    #time.sleep(2.0) # A 2-seconds "grace period" for allowing the camera to finish its setup.

    if (cap is None) or (not cap.isOpened()): # Check if the camera capture was successful or not.
        logging.error("Unable to open the specified video source, returning early.")
        return None
    else:
        logging.info("The specified camera device has successfully been opened.")


    # NOTE: Automatically determining the maximum camera resolution is not currently possible with Directshow.
    #
    #max_width = max_height = max_fps = float(0)
    #
    #default_fps =  float(cap.get(cv.CAP_PROP_FPS))
    #if (cap.set(cv.CAP_PROP_FPS, HIGH_VALUE)):
    #    max_fps = float(cap.get(cv.CAP_PROP_FPS))
    #    cap.set(cv.CAP_PROP_FPS, default_fps)
    #
    #default_width = float(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #if (cap.set(cv.CAP_PROP_FRAME_WIDTH, HIGH_VALUE)):
    #    max_width = float(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #    cap.set(cv.CAP_PROP_FRAME_WIDTH, default_width)
    #
    #default_height = float(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    #if (cap.set(cv.CAP_PROP_FRAME_HEIGHT, HIGH_VALUE)):
    #    max_height = float(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    #    cap.set(cv.CAP_PROP_FRAME_HEIGHT, default_height)
    #
    ## Restart the camera.
    #cap.release; del cap
    #cap = cv.VideoCapture(CAMERA_SOURCE, VIDEO_BACKEND)


    # TODO: The school does not allow try-expect error handling.  Use them later individually.

    cap.set(cv.CAP_PROP_FPS, CAMERA_FPS)
    # TODO: Investigate why this _has_ to be called twice with both lower and upper-case letters.
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc( *(VIDEO_CODEC.lower())) )
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc( *(VIDEO_CODEC.upper())) )
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    # NOTE: Directly capturing a video stream in grayscale mode is currently only possible on the cv.CAP_V4L backend.
    #
    #cap.set(cv.CAP_PROP_MODE, 2) # cv.CAP_MODE_GRAY = 2 = 0b10
    #cap.set(cv.CAP_PROP_CONVERT_RGB, 0)
    #cap.set(cv.CAP_PROP_FORMAT, cv.CV_8UC3)

    # Read a frame to double-check if the camera is still working fine after the configurations.
    _ret, _frame = cap.read()
    if (_ret == False) or (_frame is None): # The camera should not be returning an empty frame.
        logging.warning("Empty frames were read from the specified video source, continuing regardless.")
    else: # Everything went OK.  So we can safely notify the user of this and return afterwards.
        pass


    # TODO: Use another way (such as num_frames/elapsed_time) to programmatically get new_fps.
    new_fps = CAMERA_FPS # Should have been `int(cap.get(cv.CAP_PROP_FPS))` if it wasn't for an OpenCV bug.
    new_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    new_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # TODO: The school does not allow f-Strings with curly brackets {} for formatting the output string.  Use them later individually.
    logging.info("Camera is set-up and ready with the configurations (Width x Height @ FPS): " + str(new_width) + "x" + str(new_height) + "@" + str(new_fps))

    # And lastly, return the captured stream object.
    return cap