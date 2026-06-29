import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

SCROLL_DELAY = 0.2
CAM_WIDTH, CAM_HEIGHT = 640, 480


def detect_gestures(landmarks, handedness):
    fingers = []

    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]

    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)

    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    #Switched because the frame is flipped which caused a wrong output before
    if (handedness == "Left" and thumb_tip.x > thumb_ip.x) or \
       (handedness == "Right" and thumb_tip.x < thumb_ip.x):
        fingers.append(1)

    if len(fingers) == 5:
        return "scroll up", len(fingers)
    elif len(fingers) == 0:
        return "scroll down", len(fingers)
    else:
        return "none", len(fingers)


cam = cv.VideoCapture(0)
cam.set(3, CAM_WIDTH)
cam.set(4, CAM_HEIGHT)

last_scroll = 0
pTime = 0

print("Gesture Scroll: Scroll Up With Palm And Scroll Down With Fist")

while cam.isOpened():
    ret, frame = cam.read()

    if not ret:
        print("Error: Couldn't open the camera")
        break

    frame = cv.flip(frame, 1)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "none"
    handedness = "unknown"
    finger_count = 0

    if results.multi_hand_landmarks:
        for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):

            handedness = handedness_info.classification[0].label
            gesture, finger_count = detect_gestures(hand, handedness)

            thumb = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            distance = np.sqrt(
                (thumb.x - index.x) ** 2 +
                (thumb.y - index.y) ** 2
            )

            scroll_speed = int(np.interp(distance, [0.03, 0.25], [50, 800]))

            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            if (time.time() - last_scroll) > SCROLL_DELAY:
                if gesture == "scroll up":
                    pyautogui.scroll(scroll_speed)
                    last_scroll = time.time()

                elif gesture == "scroll down":
                    pyautogui.scroll(-scroll_speed)
                    last_scroll = time.time()

    fps = 1 / (time.time() - pTime) if (time.time() - pTime) > 0 else 0
    pTime = time.time()

    cv.putText(
        frame,
        f"FPS: {int(fps)} | Hand: {handedness} | Fingers: {finger_count} | Gesture: {gesture}",
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv.imshow("Gesture Control", frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
hands.close()
cv.destroyAllWindows()