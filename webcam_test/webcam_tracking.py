import datetime

import cv2
import imutils
import pyttsx3
import threading
import numpy as np

# Configure Webcam
vid = cv2.VideoCapture(0)

# Read First Frame
ret, firstFrame = vid.read()

if not ret:
    vid.release()

# Tracker
tracker = cv2.TrackerCSRT_create()
bbox = cv2.selectROI("Frame", firstFrame, fromCenter=False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(firstFrame, bbox)

try:
    while True:
        # Grab frame from webcam
        ret, color_frame = vid.read()

        if not ret:
            continue

        # Defining safe zone and initial text
        text = "No Alarm"
        roi = cv2.rectangle(color_frame, (50, 50), (350, 350), (0, 0, 0), 2)

        # Update tracker
        ok, bbox = tracker.update(color_frame)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(color_frame, p1, p2, (255, 0, 0), 2, 1)
            if p1[0] <= 50 or p1[1] <= 50 or p2[0] >= 350 or p2[1] >= 350:
                text = "Alarm"
        else:
            # Tracking failure
            cv2.putText(color_frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                        2)

        # draw the text and timestamp on the frame
        cv2.putText(color_frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                    2)

        # Show images
        cv2.imshow('RealSense Color Image', color_frame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    cv2.destroyAllWindows()
