import datetime

import cv2
import imutils
import pyttsx3
import threading
import numpy as np

firstFrame = None

vid = cv2.VideoCapture(0)

status_list = [None, None]
engine = pyttsx3.init()
engine.setProperty('rate', 200)


# This funtion plays the audio message
def thread_voice_alert(engine):
    engine.say("Alarm!")
    engine.runAndWait()


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


try:
    while True:
        status = 0
        # Grab frame from webcam
        ret, color_frame = vid.read()

        # resize the frame, convert it to grayscale, and blur it
        color_frame = imutils.resize(color_frame, width=500)
        gray = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # MOTION TRACKING #
        # Initialize the occupied/unoccupied text
        text = "No Alarm"
        roi = cv2.rectangle(color_frame, (50, 50), (300, 300), (0, 0, 0), 2)
        polygon1 = np.array([[50, 50], [50, 300], [300, 300], [300, 50]])

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue

            # compute the bounding box for the contour, draw it on the frame, and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            boundingRect = cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            polygon2 = np.array([[x, y], [x, y+h], [x+w, y+h], [x+w, y]])

            if check_intersection(polygon1, polygon2):
                text = "Alarm"
                status = 1
        status_list.append(status)

        # if status_list[-1] == 1 and status_list[-2] == 0:
        #     t = threading.Thread(target=thread_voice_alert, args=(engine,))
        #     t.start()

        # draw the text and timestamp on the frame
        cv2.putText(color_frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(color_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, color_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # Show images
        # cv2.imshow("Gray Image", gray)
        cv2.imshow("Security Feed", color_frame)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    engine.stop()
    cv2.destroyAllWindows()
