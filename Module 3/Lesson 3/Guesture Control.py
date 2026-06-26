import cv2 as cv
import numpy as np

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Error: Couldn't acess the camera")
    exit()
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Couldn't open the camera")
        break
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype = np.uint8)
    upper_skin = np.array([20, 255, 255], dtype = np.uint8)

    mask = cv.inRange(hsv, lower_skin, upper_skin)

    result = cv.bitwise_and(frame, frame, mask = mask)

    contours,_ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key = cv.contourArea)
        if cv.contourArea(max_contour) > 500:
            x, y, w, h = cv.boundingRect(max_contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            cv.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

    cv.imshow("Original", frame)
    cv.imshow("Filter", result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
