import cv2
import time
import mediapipe as mp
import numpy as np
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import math

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

prev_time = 0
last_action_time = 0

# Load icons (optional)
mute_icon = cv2.imread('mute.png')
unmute_icon = cv2.imread('unmute.png')

def euclidean_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def overlay_icon(frame, icon, x=1000, y=20):
    if icon is None:
        return frame
    h, w, _ = icon.shape
    frame[y:y+h, x:x+w] = icon
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    h, w, _ = frame.shape
    curr_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            if len(lm_list) >= 9:
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                distance = euclidean_distance(thumb_tip, index_tip)

                # Volume Control
                vol_level = np.clip(distance / 200, 0.0, 1.0)
                volume.SetMasterVolumeLevelScalar(vol_level, None)

                # Draw volume bar
                bar_x, bar_y = 50, 400
                bar_height = 250
                filled_height = int(vol_level * bar_height)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 30, bar_y - bar_height), (255, 255, 255), 2)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 30, bar_y - filled_height), (0, 255, 0), -1)
                cv2.putText(frame, f'Volume: {int(vol_level * 100)}%', (bar_x - 10, bar_y + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                # Mute/Unmute
                if distance < 20 and (curr_time - last_action_time > 1):
                    volume.SetMute(1, None)
                    last_action_time = curr_time
                elif distance > 100 and (curr_time - last_action_time > 1):
                    volume.SetMute(0, None)
                    last_action_time = curr_time

                # Play/Pause
                if 20 < distance < 40 and (curr_time - last_action_time > 1.5):
                    pyautogui.press('space')
                    last_action_time = curr_time

                # Screenshot
                if 40 < distance < 60 and (curr_time - last_action_time > 2):
                    screenshot_name = f"screenshot_{int(time.time())}.png"
                    cv2.imwrite(screenshot_name, frame)
                    last_action_time = curr_time

    # Show mute/unmute icon
    if volume.GetMute():
        frame = overlay_icon(frame, mute_icon)
    else:
        frame = overlay_icon(frame, unmute_icon)

    # FPS Display
    fps = int(1 / (curr_time - prev_time)) if curr_time != prev_time else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {fps}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
