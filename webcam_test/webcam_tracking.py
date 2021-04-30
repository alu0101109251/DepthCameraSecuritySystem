import cv2

# CONSTANTS
ROI = [(50, 50), (350, 350)]    # (upperLeft), (bottomRight)

# Configure Webcam
vid = cv2.VideoCapture(0)

# Read First Frame
ret, firstFrame = vid.read()

if not ret:
    vid.release()

# Tracker
tracker = cv2.TrackerCSRT_create()
bbox = None

try:
    while True:
        # Grab frame from webcam
        ret, color_frame = vid.read()

        if not ret:
            continue

        # Defining safe zone and initial text
        text = "No Alarm"
        safeZone = cv2.rectangle(color_frame, ROI[0], ROI[1], (0, 0, 0), 2)

        if bbox is not None:
            # Update tracker
            success, bbox = tracker.update(color_frame)

            # Draw bounding box
            if success:
                # Tracking success
                (x, y, w, h) = [int(p) for p in bbox]
                cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

                if x <= 50 or y <= 50 or (x + w) >= 350 or (y + h) >= 350:
                    text = "Alarm"
            else:
                # Tracking failure
                cv2.putText(color_frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # draw the text and timestamp on the frame
        cv2.putText(color_frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show images
        cv2.imshow('RealSense Color Image', color_frame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            bbox = cv2.selectROI("ROI Selector", color_frame, fromCenter=False)
            tracker.init(color_frame, bbox)
            cv2.destroyWindow("ROI Selector")

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    cv2.destroyAllWindows()
