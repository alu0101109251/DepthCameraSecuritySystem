
import pyrealsense2 as rs
import numpy as np
import cv2
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

def check_intersection(polygon1, polygon2):
    intersection = False
    for point in polygon2:
        result = cv2.pointPolygonTest(polygon1, tuple(point), measureDist=False)
        # if point inside return 1
        # if point outside return -1
        # if point on the contour return 0

        if result == 1:
            intersection = True

    return intersection

# Start streaming
pipeline.start(config)
firstFrame = None

object_detector = cv2.createBackgroundSubtractorMOG2()

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # ROI
        text = "No Alarm"
        roi = cv2.rectangle(color_image, (50, 50), (350, 350), (0, 0, 0), 2)
        polygon1 = np.array([[50, 50], [50, 350], [350, 350], [350, 50]])

        # 1. Object Detection
        mask = object_detector.apply(color_image)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 5000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                polygon2 = np.array([[x, y], [x, y + h], [x + w, y + h], [x + w, y]])

                if check_intersection(polygon1, polygon2):
                    text = "Alarm"
        # draw the text and timestamp on the frame
        cv2.putText(color_image, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(color_image, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, color_image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # Show images
        #cv2.imshow('RealSense', depth_colormap)
        cv2.imshow('RealSense Color Image', color_image)
        #cv2.imshow("Gray Image", gray)
        #cv2.imshow("Security Feed", color_frame)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
