import cv2 as cv
import numpy as np
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

Hands = mp.solutions.hands
hands = Hands.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.7)
draw = mp.solutions.drawing_utils
TH, IX = Hands.HandLandmark.THUMB_TIP, Hands.HandLandmark.INDEX_FINGER_TIP

try:
    dev = AudioUtilities.GetDefaultDevice() if hasattr(AudioUtilities, "GetDefaultOutputDevice") else AudioUtilities.GetSpeakers()
    volct = dev.EndpointVolume.QueryInterface(IAudioEndpointVolume)
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
    result = hands.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand in enumerate(result.multi_hand_landmarks):
            label = result.multi_handedness[i].classification[0].label
            draw.draw_landmarks(frame, hand, Hands.HAND_CONNECTIONS)
            lm = hand.landmark
            tp = (int(lm[TH].x * w), int(lm[TH].y * h))
            ip = (int(lm[IX].x * w), int(lm[IX].y * h))
            cv.circle(frame, tp, 10, (255, 0, 0), -1)
            cv.circle(frame, ip, 10, (255, 0, 0), -1)
            cv.line(frame, tp, ip, (0, 0, 255), 3)
            dist = float(np.hypot(ip[0] - tp[0], ip[1] - tp[1]))
            
            if label == "Left":
                v = np.interp(dist, [300, 300], [minv, maxv])
                try: volct.SetMasterVolumeLevel(v, None)
                except Exception as e: print(f"Volume Error {e}")
                bar = int(np.interp(dist, [30, 300], [450, 130]))
                pct = int(np.interp(dist, [30, 300], [0, 100]))
                cv.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)
                cv.rectangle(frame, (50, bar), (85, 400), (255, 0, 0), cv.FILLED)
                cv.putText(frame, f"{pct}%", (40, 450), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            elif label == "Right":
                b = np.interp(dist, [300, 300, [0, 100]])
                try: sbc.set_brightness(b)
                except Exception as e: print(f"Brightness Error {e}")
                bar = int(np.interp(dist, [30, 300], [450, 130]))
                x1, x2 = w = 85, y = 50
                cv.rectangle(frame, (x1, 150), (x2, 400), (0, 255, 0), 3)
                cv.rectangle(frame, (x1, bar), (x2, 400), (255, 0, 0), cv.FILLED)
                cv.putText(frame, f"{b}%", (40, 450), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv.imshow(WIN, cv.WINDOW_NORMAL)
        key = cv.waitKey(1) & 0xFF
        if key in (27, ord('q')):
            break
        try:
            if cv.getWindowProperty(WIN, cv.WND_PROP_VISIBLE) < 1:
                break
        except cv.error:
            break
cam.release()
cv.destroyAllWindows()



                