✋ Gesture-Controlled Volume Controller
Control your system volume and media playback without touching your keyboard or mouse — just use hand gestures detected via webcam!

🧠 Features
🔊 Volume Control – Move thumb and index finger apart to increase volume, bring them close to lower it

🔇 Mute – Left hand pinch gesture mutes audio

⏯️ Play/Pause Media – Use pinch gesture to simulate the Space key

📸 Screenshot Capture – Pinch gesture takes a snapshot of the current frame

📈 Real-Time FPS Display

✋ Supports dual-hand detection

📦 Tech Stack
Python

MediaPipe – Hand landmark detection

OpenCV – Webcam capture and drawing utilities

PyCaw – Control system audio on Windows

PyAutoGUI – Trigger play/pause actions

comtypes, ctypes – Windows API handling

📷 How It Works
Uses MediaPipe to detect 21 key points (landmarks) on each hand

Tracks the distance between thumb and index finger

Maps the distance to a volume scalar value using interpolation

Uses pycaw to set system volume on Windows

Implements gesture logic for mute, screenshot, and media controls

🖥️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/rashprit/gesture-volume-controller.git
cd gesture-volume-controller
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # Windows
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Or manually:

bash
Copy
Edit
pip install mediapipe opencv-python numpy pycaw pyautogui comtypes
4. Run the project
bash
Copy
Edit
python gesture_volume_control.py
✅ Requirements
OS: Windows (required for Pycaw to control system audio)

Python: 3.8–3.11 (MediaPipe may not support 3.13 yet)

Webcam

📸 Example

![alt text](../screenshot_1750652646.png)
Live webcam with real-time landmarks and volume bar

🛠️ Potential Enhancements
Add GUI for toggling gestures

Add gesture-controlled brightness / screen capture

Deploy as a standalone app with PyInstaller

Cross-platform support (e.g., using platform-specific audio APIs)

🤝 Contributing
Pull requests are welcome! Open an issue to discuss what you’d like to add or improve.

📄 License
This project is open-source under the MIT License.

🙌 Acknowledgements
Google MediaPipe

PyCaw

