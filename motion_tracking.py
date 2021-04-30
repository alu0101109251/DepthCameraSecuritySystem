import pyrealsense2 as rs
import numpy as np
import cv2


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
frames = pipeline.wait_for_frames()
firstFrame = np.asanyarray(frames.get_color_frame().get_data())

if firstFrame is None:
    pipeline.stop()
    exit(1)

# Tracker
tracker = cv2.TrackerCSRT_create()
bbox = cv2.selectROI("Frame", firstFrame, fromCenter=False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(firstFrame, bbox)

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
        roi = cv2.rectangle(colorFrame, (50, 50), (350, 350), (0, 0, 0), 2)

        # Update tracker
        ok, bbox = tracker.update(colorFrame)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(colorFrame, p1, p2, (255, 0, 0), 2, 1)
            if p1[0] <= 50 or p1[1] <= 50 or p2[0] >= 350 or p2[1] >= 350:
                text = "Alarm"
        else:
            # Tracking failure
            cv2.putText(colorFrame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # draw the text and timestamp on the frame
        cv2.putText(colorFrame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show images
        cv2.imshow('RealSense Color Image', colorFrame)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    pipeline.stop()
    cv2.destroyAllWindows()
