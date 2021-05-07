import cv2
import winsound
import threading

# Safe Zone Coordinates
(szx, szy, szw, szh) = (50, 50, 300, 300)

# Configure Webcam
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Tracker
tracker = cv2.TrackerCSRT_create()
bbox = None
alarmList = [None, None]


def beep():
    winsound.Beep(frequency=2500, duration=750)


try:
    while True:
        # Grab frame from webcam
        ret, colorFrame = vid.read()
        cv2.flip(colorFrame, 1, colorFrame)
        alarm = 0

        if not ret:
            continue

        # Defining safe zone and initial text
        text = "No Alarm"
        safeZone = cv2.rectangle(colorFrame, (szx, szy), (szx + szw, szy + szh), (0, 0, 255), 2, 1)

        if bbox is not None:
            # Update tracker
            success, bbox = tracker.update(colorFrame)

            # Draw bounding box
            if success:
                # Tracking success
                (x, y, w, h) = [int(p) for p in bbox]
                cv2.rectangle(colorFrame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

                if x <= szx or y <= szy or (x + w) >= (szx + szw) or (y + h) >= (szy + szh):
                    text = "Alarm"
                    alarm = 1

            else:
                # Tracking failure
                cv2.putText(colorFrame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        alarmList.append(alarm)
        if alarmList[-1] == 1 and alarmList[-2] == 0:
            threading.Thread(target=beep()).start()

        # draw the text and timestamp on the frame
        cv2.putText(colorFrame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            bbox = cv2.selectROI("ROI Selector", colorFrame, fromCenter=False)
            tracker.init(colorFrame, bbox)
            cv2.destroyWindow("ROI Selector")

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    cv2.destroyAllWindows()
