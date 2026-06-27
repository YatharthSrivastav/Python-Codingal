import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Error: Coundn't open the camera")
    exit()
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to load the camera")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30))
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, f"Number Of People: {len(faces)}", (10, 30), font, 1, (255, 0 , 0), 2, cv.LINE_AA )
    cv.imshow("Face Tracking And People Counter", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
