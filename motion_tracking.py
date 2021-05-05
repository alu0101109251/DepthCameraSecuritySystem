import pyrealsense2 as rs
import numpy as np
import cv2

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

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        colorFrame = frames.get_color_frame()

        if not colorFrame:
            continue

        # Convert images to numpy arrays
        colorFrame = np.asanyarray(colorFrame.get_data())

        # Defining safe zone and initial text
        text = "No Alarm"
        safeZone = cv2.rectangle(colorFrame, (szx, szy), (szx + szw, szy + szh), RED, 2, 1)

        if bbox is not None:
            # Update tracker
            success, bbox = tracker.update(colorFrame)

            # Draw bounding box
            if success:
                # Tracking success
                (x, y, w, h) = [int(p) for p in bbox]
                cv2.rectangle(colorFrame, (x, y), (x + w, y + h), GREEN, 2, 1)

                if is_out_of_bounds(x, y, w, h):
                    text = "Alarm"
            else:
                # Tracking failure
                cv2.putText(colorFrame, "Tracking failure!", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)

        # draw the text and timestamp on the frame
        cv2.putText(colorFrame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLUE, 2)
        cv2.putText(colorFrame, "CSRT Tracker", (10, colorFrame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, BLUE, 1)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            bbox = cv2.selectROI("BBOX Selector", colorFrame, fromCenter=False)
            tracker.init(colorFrame, bbox)
            cv2.destroyWindow("BBOX Selector")

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
