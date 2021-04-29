import datetime

import cv2
import imutils
import numpy as np
import pyrealsense2 as rs

def is_outside_safezone(safezone, object):
    outside = False

    return outside

# Constants
AREA_THRESHOLD = 10000

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
firstFrame = None

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        security_image = color_image.copy()

        # Convert it to grayscale, and blur it
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # gray = cv2.normalize(gray, gray, 0, 255, cv2.NORM_MINMAX)

        # Defining safe zone and initial text
        text = "No Alarm"
        roi = cv2.rectangle(security_image, (50, 50), (350, 350), (0, 0, 0), 2)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < AREA_THRESHOLD:
                continue

            # compute the bounding box for the contour, draw it on the frame, and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            boundingRect = cv2.rectangle(security_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # polygon2 = np.array([[x, y], [x, y+h], [x+w, y+h], [x+w, y]])

            if x <= 50 or y <= 50 or (x+w) >= 350 or (y+h) >= 350:
                text = "Alarm"

        # draw the text and timestamp on the frame
        cv2.putText(security_image, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(security_image, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, security_image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # Show images
        cv2.imshow("Security Feed", security_image)
        cv2.imshow("First Frame", firstFrame)
        cv2.imshow("Gray", gray)
        cv2.imshow("Frame Delta", frameDelta)
        cv2.imshow("Thresh", thresh)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    cv2.destroyAllWindows()
