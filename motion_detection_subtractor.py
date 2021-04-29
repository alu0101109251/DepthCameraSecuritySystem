
import pyrealsense2 as rs
import numpy as np
import cv2
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time

# Constants
AREA_THRESHOLD = 5000

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
firstFrame = None

# Background Subtraction
background_subtractor = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Defining safe zone and initial text
        text = "No Alarm"
        roi = cv2.rectangle(color_image, (50, 50), (350, 350), (0, 0, 0), 2)

        # Foreground Mask
        mask = None
        mask = background_subtractor.apply(color_image, mask, 0.0)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
        # _, mask = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # Calculate area and remove small elements
            if cv2.contourArea(cnt) < AREA_THRESHOLD:
                continue

            # compute the bounding box for the contour, draw it on the frame, and update the text
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if x <= 50 or y <= 50 or (x+w) >= 350 or (y+h) >= 350:
                text = "Alarm"

        # draw the text and timestamp on the frame
        cv2.putText(color_image, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show images
        cv2.imshow('Foreground Mask', mask)
        cv2.imshow('RealSense Color Image', color_image)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
