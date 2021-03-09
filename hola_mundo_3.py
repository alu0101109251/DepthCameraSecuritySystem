
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

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HSV)

        # Stack both images horizontally
        # images = np.vstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', depth_colormap)
        # blob detector
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        # gray_image = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2GRAY)
        # gray_image = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('gray image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow("gray image", gray_image)

        # BLOB DETECTOR
        # Set up the detector with default parameters.
        # function para version opencv > 3
        params = cv2.SimpleBlobDetector_Params()
        print(' Parametros', params.maxArea)
        detector = cv2.SimpleBlobDetector_create()
        overlay = color_image.copy()

        # Detect blobs.
        # keypoints = detector.detect(color_image)
        keypoints = detector.detect(gray_image)

        # # Draw detected blobs as red circles.
        # # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(gray_image, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # # Show keypoints
        cv2.namedWindow('Keypoints', cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Keypoints", im_with_keypoints)

        cv2.namedWindow('RealSense Color imagen', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense Color imagen', color_image)

        for k in keypoints:
            cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), -1)
            cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
            cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)

        opacity = 0.5
        cv2.addWeighted(overlay, opacity, color_image, 1 - opacity, 0, color_image)

        # Uncomment to resize to fit output window if needed
        # im = cv2.resize(im, None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        cv2.imshow("Output", color_image)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        cv2.waitKey(1)

finally:

    # Stop streaming
    print(' key points', im_with_keypoints)
    pipeline.stop()
