import cv2 as cv
import numpy as np
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndPointVolume
import screen_brightness_control as sbc

Hands = mp.solutions.hands
hands = Hands.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.7)
draw = mp.solutions.drawing_utils
TH, IX = Hands.HandLandmark.THUMB_TIP, Hands.HandLandmark.INDEX_FINGER_TIP

try:
    dev = AudioUtilities.GetDefaultDevice() if hasattr(AudioUtilities, "GetDefaultOutputDevice") else AudioUtilities.GetSpeakers()
    volct = dev.EndpointVolume.QueryInterface(IAudioEndPointVolume)
    minv, maxv = volct.GetVolumeRange()[:2]
except:
    print("Error")
    exit()

cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Error: Couldn't acess camera")
    exit()

WIN = "Hand Guesture Control"
cv.namedWindow(WIN, cv.WINDOW_NORMAL)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Couldn't open camera")
        break
    frame = cv.flip(frame, 1)
    h, w = frame.shape[:2]
    result = hands.process(cv.cvtColor(cv.COLOR_BGR2RGB))

    if result.multi_hand_landmarks and result.multi.handedness:
        for i in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label
            draw.draw_landmarks(frame, hands, Hands.HAND_CONNECTIONS)
            lm = hands.landmark
            tp = int(lm[TH].x*w, lm[TH].y*h)
            ip = int(lm[IX].x*w, lm[IX].y*h)
            cv.circle(frame, tp, 10, (255, 0, 0), -1)
            cv.circle(frame, ip, 10, (255, 0, 0), -1)
            cv.line(frame, tp, ip, (0, 0, 255), 3)
            dist = float(np.hypot(ip[0] - tp[0], ip[1] - tp[1]))
            
