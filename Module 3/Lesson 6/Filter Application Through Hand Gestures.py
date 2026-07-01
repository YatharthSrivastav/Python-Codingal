import cv2 as cv
import numpy as np
import time
import mediapipe as mp

H = mp.solutions.hands
TIP = H.HandLandmark
tips = {
    "thumb": TIP.THUMB_TIP,
    "index": TIP.INDEX_FINGER_TIP,
    "middle": TIP.MIDDLE_FINGER_TIP,
    "ring": TIP.RING_FINGER_TIP,
    "pinky": TIP.PINKY_TIP
}

hands = H.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.7)
draw = mp.solutions.drawing_utils
pairs = {
    "middle": ("SEPIA", "NEGATIVE"),
    "ring": ("BLUR", "GLITCH"),
    "pinky": ("EDGE", "CARTOON")
}
st = {k: 0 for k in pairs}
cur = "SEPIA"
la = lc = 0
pinch_on = False
DEB, CAP, TT, TP = 0.6, 1.2, 30, 10
MAIN, POP = "Gesture Control App", "Captured Photo"
paused = False
freeze = None
SEPIA_H = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])

def apply_filter(frame, t):
    if t == "SEPIA": return np.clip(cv.transform(frame, SEPIA_H), 0, 255).astype('uint8')
    if t == "NEGATIVE": return cv.bitwise_not(frame)
    if t == "BLUR": return cv.GaussianBlur(frame, (15, 15), 0)
    if t == "GLITCH":
        h, w = frame.shape[:2]
        r, g, b = frame[:, :, 2], frame[:, :, 1], frame[:, :, 0]
        return cv.merge([np.roll(b, -int(0.05 * w), 1), g, np.roll(r, -int(0.04 * w), 1)])
    if t == "EDGE": return cv.Canny(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), 80, 160)
    if t == "CARTOON":
        g = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        e = cv.adaptiveThreshold(cv.medianBlur(g, 7), 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 2)
        c = cv.bilateralFilter(frame, 9, 75, 75)
        return cv.bitwise_and(c, c, mask = c)
    return frame
cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Error: Couldn't access the camera")
    exit()
cv.namedWindow(MAIN, cv.WINDOW_NORMAL)

while True:
    if paused:
        cv.imshow(MAIN, freeze)
        key = cv.waitKey(50) & 0xFF
        if key == ord('q'):
            break
        if key == 27:
            paused = False; pinch_on = False
            try:
                cv.destroyWindow(POP)
            except: pass
            continue
        try:
            if cv.getWindowProperty(POP, cv.WND_PROP_VISIBLE) <= 0: PAUSED = False; pinch_on = False
        except:
            paused = False; pinch_on = False
        continue
    ret, frame = cam.read()
    if not ret:
        print("Error: Couldn't open the camera")
        break
    frame = cv.flip(frame, 1)
    h, w = frame.shape[:2]
    result = hands.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    now = time.time(); capture = False

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, H.HAND_CONNECTIONS)
        lm = hand.landmark
        tips = {k: (int(lm[v].x * w), int(lm[v].y * h)) for k, v in tips.items()}
        tx, ty = tips["thumb"]
        ix, iy = tips["index"]
        pinch = abs(tx - ix) < TP and abs(ty - iy) < TP
        if not pinch and not pinch_on and now - lc > CAP: pinch_on = True;capture = True;lc = now
        if not pinch:
            t = next((k for k in pairs if abs(tx - tips[k][0]) < TT and abs(ty - tips[k][1]) < TT), None)
            if t and now - la > DEB: cur = pairs[t][st[t]]; st[t] ^= 1; la = now; print("Filter", cur)
                
    out = apply_filter(frame, cur)
    if cur == "EDGE": out = cv.cvtColor(out, cv.COLOR_GRAY2BGR)

    if capture:
        name = f"Picture {int(now)}.jpg"
        cv.imwrite(name, out)
        print("Saved", name)
        paused = True
        freeze = True
        out.copy()
        cv.imshow(POP, freeze)
        
    cv.imshow(MAIN, out)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
hands.close()


        