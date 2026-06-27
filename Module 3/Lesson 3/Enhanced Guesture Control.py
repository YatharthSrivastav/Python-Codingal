import cv2 as cv
import numpy as np
import mediapipe as mp

def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended = 0

    if abs(landmarks[tip_ids[0]].x - landmarks[pip_ids[0]].x) > 0.04:
        extended += 1

    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            extended += 1
    if extended >= 4:
        return "Open"

    elif extended <= 1:
        return "Closed Fist"

    else:
        return "Partial"

shape_x, shape_y, shape_size = 200, 200, 50

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Error: Couldn't acess the camera")
    exit()
while True:
    ret, frame = cam.read()
    frame = cv.flip(frame, 1)
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

            shape_x = center_x
            shape_y = center_y
    cv.circle(frame, (shape_x, shape_y), shape_size, (0, 0, 255), -1)

    cv.imshow("Original", frame)
    cv.imshow("Filter", result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
