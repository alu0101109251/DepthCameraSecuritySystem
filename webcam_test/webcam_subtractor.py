import datetime

import cv2
import imutils
import pyttsx3
import threading
import numpy as np

# Constants
AREA_THRESHOLD = 5000

# Configure Webcam
vid = cv2.VideoCapture(0)

# Background Subtraction
background_subtractor = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=25, detectShadows=True)

while cv2.waitKey(40) != ord(' '):
    ret, tempFrame = vid.read()
    cv2.imshow("Background Detection", tempFrame)
    background_subtractor.apply(tempFrame, 0.5)

cv2.destroyWindow("Background Detection")

try:
    while True:
        # Grab frame from webcam
        ret, colorFrame = vid.read()
        mask = None

        if not ret:
            continue

        # Defining safe zone and initial text
        text = "No Alarm"
        roi = cv2.rectangle(colorFrame, (50, 50), (350, 350), (0, 0, 0), 2)

        # Foreground Mask
        mask = background_subtractor.apply(colorFrame, mask, 0.0)
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
            cv2.rectangle(colorFrame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if x <= 50 or y <= 50 or (x + w) >= 350 or (y + h) >= 350:
                text = "Alarm"
        # draw the text and timestamp on the frame
        cv2.putText(colorFrame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)
        cv2.imshow('Foreground Mask', mask)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    cv2.destroyAllWindows()
