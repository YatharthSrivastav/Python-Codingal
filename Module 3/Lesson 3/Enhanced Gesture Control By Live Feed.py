import cv2 as cv
import numpy as np
import mediapipe as mp
import sys 
sys.modules['tensorflow'] = None

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- Global Canvas/Shape Properties ---
shape_x, shape_y = 300, 300
shape_size = 50
shape_color = (0, 0, 255)  # Default: Red
prev_x, prev_y = None, None
direction = "Stationary"

# --- Task 1: Direction Tracking Function ---
def detect_direction(curr_x, curr_y, prev_x, prev_y):
    if prev_x is None or prev_y is None:
        return "Stationary"
    
    dx = curr_x - prev_x
    dy = curr_y - prev_y
    threshold = 8  # Minimum pixel movement to register direction
    
    dir_components = []
    if abs(dx) > threshold:
        dir_components.append("Right" if dx > 0 else "Left")
    if abs(dy) > threshold:
        dir_components.append("Down" if dy > 0 else "Up")
        
    return " ".join(dir_components) if dir_components else "Stationary"

# --- Task 2: Extended Gesture Detection Function ---
def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended = []

    # Thumb tracking (horizontal check)
    if abs(landmarks[4].x - landmarks[2].x) > 0.04:
        extended.append(True)
    else:
        extended.append(False)

    # Index, Middle, Ring, Pinky tracking (vertical check)
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            extended.append(True)
        else:
            extended.append(False)

    extended_count = sum(extended)

    if extended_count >= 4:
        return "Open Hand"
    elif extended_count == 1 and extended[0] and landmarks[4].y < landmarks[2].y:
        return "Thumbs Up"
    elif extended_count <= 1:
        return "Closed Fist"
    else:
        return "Partial"

# --- Task 3: Dynamic Size/Distance Calculation Function ---
def calculate_dynamic_size(hand_landmarks, w, h):
    # Use Euclidean distance between Wrist (0) and Middle Finger Base (9) as a depth proxy
    wrist = hand_landmarks.landmark[0]
    middle_base = hand_landmarks.landmark[9]
    
    x0, y0 = wrist.x * w, wrist.y * h
    x9, y9 = middle_base.x * w, middle_base.y * h
    
    distance = np.sqrt((x0 - x9)**2 + (y0 - y9)**2)
    # Scale distance to an appropriate object pixel size (clamped between 20 and 150)
    return int(max(20, min(distance * 0.8, 150)))


# --- Main Application Loop ---
cam = cv.VideoCapture(0)

# Task 4: Basic Error Handling for camera source
if not cam.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Program Started! Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    
    # Task 4: Error Handling if frame capture fails temporarily
    if not ret:
        print("Warning: Failed to grab frame.")
        continue

    frame = cv.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    gesture = "No hand detected"
    
    # Check if any hands are detected
    if results.multi_hand_landmarks:
        # Task 4: Simple logic handles the primary detected hand safely
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # 1. Track Movement Position using Index Finger Tip (Landmark 8)
        index_tip = hand_landmarks.landmark[8]
        curr_x, curr_y = int(index_tip.x * w), int(index_tip.y * h)
        
        # Task 1: Track Direction & Update Shape Position
        direction = detect_direction(curr_x, curr_y, prev_x, prev_y)
        shape_x, shape_y = curr_x, curr_y
        prev_x, prev_y = curr_x, curr_y
        
        # Task 2: Recognize Gesture
        gesture = detect_gesture(hand_landmarks)
        
        # Task 2 Action: Dynamically update shape color based on current gesture
        if gesture == "Open Hand":
            shape_color = (0, 255, 0)     # Green
        elif gesture == "Closed Fist":
            shape_color = (0, 0, 255)     # Red
        elif gesture == "Thumbs Up":
            shape_color = (255, 0, 0)     # Blue
        else:
            shape_color = (0, 165, 255)   # Orange for partial
            
        # Task 3 Action: Dynamically update shape size based on distance
        shape_size = calculate_dynamic_size(hand_landmarks, w, h)
        
        # Draw skeleton connections
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
    else:
        # Task 4 Error Handling: Reset tracking states safely when hand is lost
        prev_x, prev_y = None, None
        direction = "Stationary"

    # --- Render UI Overlays and Shapes ---
    # Draw the controlled dynamic shape
    cv.circle(frame, (shape_x, shape_y), shape_size, shape_color, -1)
    
    # Text Overlays
    cv.putText(frame, f"Gesture: {gesture}", (10, 40), 
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv.putText(frame, f"Direction: {direction}", (10, 80), 
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv.putText(frame, f"Object Size: {shape_size}", (10, 120), 
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv.imshow("Interactive Hand Tracking", frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()