# This file is part of AIMER.
# 
# AIMER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# AIMER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AIMER.  If not, see <https://www.gnu.org/licenses/>.

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
