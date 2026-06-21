import cv2 as cv
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import dlib

#I had used dlib before and it was giving better performance than haarcascade and also wasn't drawing 2 bounding boxes on the same person - one on face and one on mouth(ocassionally).
# face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
# if face_cascade.empty():
#     print("Error loading Haar cascade")


face_detector = dlib.get_frontal_face_detector()

emotion_label = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
emotion_model = tf.keras.models.load_model("Module 2\\Lesson 6\\emotion_model.h5", compile=False)

def emotion_analysis(frame, gray, x, y, w, h):
    roi_gray = gray[y:y + h, x:x + w]
    if roi_gray.size == 0:
        return

    roi_resized = cv.resize(roi_gray, (48, 48))
    roi_resized = roi_resized.astype('float32') / 255
    roi_resized = img_to_array(roi_resized)
    roi_resized = np.expand_dims(roi_resized, axis=0)

    emotion_pred = emotion_model.predict(roi_resized)
    max_index = np.argmax(emotion_pred[0])
    predicted_emotion = emotion_label[max_index]

    cv.putText(frame, predicted_emotion, (x, y - 10),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


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

    # faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    faces = face_detector(rgb)

    for face in faces:
        x = face.left()
        y = face.top()
        w = face.right() - x
        h = face.bottom() - y

        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        emotion_analysis(frame, gray, x, y, w, h)

    cv.imshow("Face And Emotion Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()