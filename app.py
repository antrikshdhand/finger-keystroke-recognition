import numpy as np
import cv2 as cv

### CLICKS MUST BE FROM POINT (0,0) to (1, 0) to (0, 1) to (1, 1)
### OTHERWISE IT WON'T WARP PROPERLY

# List to store mouse clicks
clicks = []

# Dimensions of warped image
width = 1280
height = 720

def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        if len(clicks) < 4:
            point = [x, y]
            clicks.append(point)
        return

# Begin webcam capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    for i in range(len(clicks)):
        cv.circle(frame, (clicks[i][0], clicks[i][1]), 5, (0, 0, 255), cv.FILLED)

    if (len(clicks) == 4):
        pts = np.array(clicks, np.float32)
        ideal_pts = np.array([[0, 0], [width, 0], [0, height], [width, height]], np.float32)
        warp_matrix = cv.getPerspectiveTransform(pts, ideal_pts)
        warped_frame = cv.warpPerspective(frame, warp_matrix, (width, height))
        cv.imshow('Warped frame', warped_frame)

        # cv.polylines(frame, [pts], True, (0, 255, 0), 3)
        # cv.rectangle(frame, (clicks[0][0], clicks[0][1]), (clicks[1][0], clicks[1][1]), (0, 255, 0), 3)

    # Display the resulting frames
    cv.imshow('Original frame', frame)

    # Set mouse handler for the image
    cv.setMouseCallback('Original frame', click_event)

    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()