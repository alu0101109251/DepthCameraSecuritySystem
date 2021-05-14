#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Motion Detection using Image Difference."""

import cv2
import numpy as np
import pyrealsense2 as rs

__author__ = "Javier Alonso Delgado"
__license__ = "CC-BY-SA-4.0"
__version__ = "1.0"
__email__ = "alu0101109251@ull.edu.es"

# Constants
AREA_THRESHOLD = 10000
RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)

# Safe Zone Coordinates
(szx, szy, szw, szh) = (50, 50, 300, 300)


# Check is rectangle is out of safe zone
def is_out_of_bounds(px, py, weight, height):
    if px <= szx or py <= szy or (px + weight) >= (szx + szw) or (py + height) >= (szy + szh):
        return True
    return False


# Intel RealSense Camera Pipeline Configuration
pipeline = rs.pipeline(ctx=rs.context())
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Initialize first frame
firstFrame = None

# Press SPACE to select the background frame
while cv2.waitKey(40) != ord(' '):
    frames = pipeline.wait_for_frames()
    firstFrame = np.asanyarray(frames.get_color_frame().get_data())
    cv2.imshow("Background Selection", firstFrame)

firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
cv2.destroyWindow("Background Selection")

try:
    while True:

        # Wait for coherent frames and grab color frame
        frames = pipeline.wait_for_frames()
        colorFrame = frames.get_color_frame()

        # Check if a frame was successfully received
        if not colorFrame:
            continue

        # Convert image to numpy arrays
        colorFrame = np.asanyarray(colorFrame.get_data())

        # Convert it to grayscale and blur it
        grayFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
        grayFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)
        # gray = cv2.normalize(gray, gray, 0, 255, cv2.NORM_MINMAX)

        # Draw safe zone and set initial status text
        text = "Safe"
        safeZone = cv2.rectangle(colorFrame, (szx, szy), (szx + szw, szy + szh), RED, 2, 1)

        # Compute the absolute difference between current frame and first frame
        deltaFrame = cv2.absdiff(firstFrame, grayFrame)

        # Threshold the image and clean up
        threshFrame = cv2.threshold(deltaFrame, 25, 255, cv2.THRESH_BINARY)[1]
        # thresh = cv2.adaptiveThreshold(deltaFrame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        threshFrame = cv2.dilate(threshFrame, None, iterations=2)

        # Grab and filter contours.
        contours, _ = cv2.findContours(threshFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            # Calculate area and remove small elements
            if cv2.contourArea(c) < AREA_THRESHOLD:
                continue

            # Compute the bounding box for the contour and draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(colorFrame, (x, y), (x + w, y + h), GREEN, 2, 1)

            # Check if the bounding box is out of the safe zone
            if is_out_of_bounds(x, y, w, h):
                text = "Alarm"

        # Draw status text and detection technique in the frame
        cv2.putText(colorFrame, "Zone Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLUE, 2)
        cv2.putText(colorFrame, "Absolute Difference Motion Detection", (10, colorFrame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, BLUE, 1)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)
        # cv2.imshow("First Frame", firstFrame)
        # cv2.imshow("Gray Frame", grayFrame)
        # cv2.imshow("Delta Frame", deltaFrame)
        # cv2.imshow("Thresh Frame", threshFrame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # If the `q` key is pressed, break from the loop
        if key == ord("q"):
            break

finally:

    # Cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
