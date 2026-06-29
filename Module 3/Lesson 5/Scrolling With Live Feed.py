import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)
mp_drawing = mp.solutions.drawing_utils

SCROLL_SPEED = 300
SCROLL_DELAY = 1
CAM_WIDTH, CAM_HEIGHT = 640, 480

def detect_gestures(landmarks, handedness):
    fingers = []
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if (handedness == 'right' and thumb_tip.x > thumb_ip.x) or (handedness == 'left' and thumb_tip.x > thumb_ip.y):
        fingers.append(1)

    return "scroll up" if sum(fingers) == '5' else "scroll down" if len(fingers) == 0 else "none" 

cam = cv.VideoCapture(0)
cam.set(3, CAM_WIDTH)
cam.set(4, CAM_HEIGHT)
last_scroll = pTime = 0
print("Gesture Scroll: Scroll Up With Palm And Scroll Down With Fist")

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        print("Error: Couldn't open the camera")
        break
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame = cv.flip(rgb, 1)
    results = hands.process(frame)
    gesture, handedness = 'none', 'unknown'
    if results.multi_hand_landmarks:
        for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            handedness = handedness_info.classification[0].label
            gesture = detect_gestures(hand, handedness)
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            if (time.time() - last_scroll) > SCROLL_DELAY:
                if gesture == "scroll up": pyautogui.scroll(SCROLL_SPEED)
                elif gesture == "scroll down": pyautogui.scroll(-SCROLL_SPEED)
                last_scroll = time.time()

    fps = 1/(time.time()-pTime) if (time.time()-pTime) > 0 else 0
    pTime = time.time()
    cv.putText(frame, f"FPS: {int(fps)} | Hand: {handedness} | Gesture: {gesture}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), cv.LINE_AA)
    cv.imshow("Gesture Controll", cv.cvtColor(frame, cv.COLOR_RGB2BGR))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()