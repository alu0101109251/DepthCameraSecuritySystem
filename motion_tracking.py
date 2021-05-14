#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Motion Tracking using CSRT Tracker."""

import pyrealsense2 as rs
import numpy as np
import cv2

__author__ = "Javier Alonso Delgado"
__license__ = "CC-BY-SA-4.0"
__version__ = "1.0"
__email__ = "alu0101109251@ull.edu.es"

# CONSTANTS
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

# Tracker
tracker = cv2.TrackerCSRT_create()
bbox = None

try:
    while True:

        # Wait for coherent frames and grab color frame
        frames = pipeline.wait_for_frames()
        colorFrame = frames.get_color_frame()

        # Check if a frame was successfully received
        if not colorFrame:
            continue

        # Convert images to numpy arrays
        colorFrame = np.asanyarray(colorFrame.get_data())

        # Draw safe zone and set initial status text
        text = "Safe"
        safeZone = cv2.rectangle(colorFrame, (szx, szy), (szx + szw, szy + szh), RED, 2, 1)

        # Check if tracker is initialized
        if bbox is not None:
            # Update tracker
            success, bbox = tracker.update(colorFrame)

            # Tracking Success
            if success:
                # Grab the bounding box and draw it on the frame
                (x, y, w, h) = [int(p) for p in bbox]
                cv2.rectangle(colorFrame, (x, y), (x + w, y + h), GREEN, 2, 1)

                # Check if the bounding box is out of the safe zone
                if is_out_of_bounds(x, y, w, h):
                    text = "Alarm"

            # Tracking failure
            else:
                cv2.putText(colorFrame, "Tracking failure!", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)

        # Draw status text and detection technique in the frame
        cv2.putText(colorFrame, "Zone Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLUE, 2)
        cv2.putText(colorFrame, "CSRT Tracker", (10, colorFrame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, BLUE, 1)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to select ROI to track.
        # Make selection using the mouse and press ENTER or SPACE
        if key == ord("s"):
            bbox = cv2.selectROI("BBOX Selector", colorFrame, fromCenter=False)
            tracker.init(colorFrame, bbox)
            cv2.destroyWindow("BBOX Selector")

        # If the `q` key is pressed, break from the loop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
