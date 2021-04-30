import cv2
import imutils

# Constants
AREA_THRESHOLD = 10000

# Safe Zone Coordinates
(szx, szy, szw, szh) = (50, 50, 300, 300)


# Check is rectangle is out of safe zone
def is_out_of_bounds(px, py, weight, height):
    if px <= szx or py <= szy or (px + weight) >= (szx + szw) or (py + height) >= (szy + szh):
        return True
    return False


# Configure Webcam
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize first frame
firstFrame = None

try:
    while True:
        # Grab frame from webcam
        ret, colorFrame = vid.read()
        mask = None

        if not ret:
            continue

        securityFrame = colorFrame.copy()

        # Convert it to grayscale, and blur it
        gray = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # gray = cv2.normalize(gray, gray, 0, 255, cv2.NORM_MINMAX)

        # Defining safe zone and initial text
        text = "No Alarm"
        safeZone = cv2.rectangle(securityFrame, (szx, szy), (szx + szw, szy + szh), (0, 0, 255), 2, 1)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]
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
            boundingRect = cv2.rectangle(securityFrame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

            if is_out_of_bounds(x, y, w, h):
                text = "Alarm"

        # draw the text and timestamp on the frame
        cv2.putText(securityFrame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Show images
        cv2.imshow("Security Feed", securityFrame)
        cv2.imshow("First Frame", firstFrame)
        cv2.imshow("Gray", gray)
        cv2.imshow("Thresh", thresh)

        # Record if the user presses a key
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

finally:

    # cleanup the camera and close any open windows
    vid.release()
    cv2.destroyAllWindows()
