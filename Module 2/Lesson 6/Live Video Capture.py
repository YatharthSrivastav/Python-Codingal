import cv2 as cv
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Error: Couldn't open camera")
    exit()
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture video")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minSize=(30, 30), minNeighbors=5)
    for (x, w, y, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
    cv.imshow("Face Detection Press q to quit", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()


