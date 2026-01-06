Air Writing Application - Phase 1: Hand Detection & Tracking
Overview
Phase 1 implements real-time hand detection and tracking using MediaPipe's robust hand landmark detection. The system tracks the index finger tip in real-time and visualizes all hand landmarks on the video feed.
Features Implemented ✅

✅ Real-time camera access and frame capture
✅ Robust hand detection using MediaPipe
✅ 21-point hand landmark tracking
✅ Index finger tip tracking with visual indicator
✅ Real-time FPS display
✅ Hand detection status feedback
✅ Smooth performance at 30+ FPS

Project Structure
air-writing-app/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py                          # Main application entry point
│   ├── camera/
│   │   └── camera_stream.py             # Camera handling
│   ├── hand_tracking/
│   │   ├── hand_detector.py             # Hand detection logic
│   │   └── landmark_utils.py            # Landmark utilities
│   └── utils/
│       └── config.py                    # Configuration settings
Installation
Prerequisites

Python 3.8 or higher
Webcam/camera device
pip package manager

Setup Instructions

Clone or create the project directory

bashmkdir air-writing-app
cd air-writing-app

Create the folder structure

bashmkdir -p src/camera src/hand_tracking src/utils
touch src/__init__.py
touch src/camera/__init__.py
touch src/hand_tracking/__init__.py
touch src/utils/__init__.py

Install dependencies

bashpip install -r requirements.txt
Usage
Running the Application
bashpython -m src.main
Controls

q or ESC - Quit the application

What You'll See

Live camera feed with mirror effect
Green hand landmarks drawn on detected hands
Yellow circle indicator on index finger tip
FPS counter (top left)
Hand detection status
Index finger tip coordinates

Technical Details
Hand Detection

Uses MediaPipe Hands solution
Detects up to 1 hand (configurable)
21 hand landmarks per hand
Real-time tracking at 30+ FPS

Landmarks
MediaPipe provides 21 hand landmarks:

Landmark 0: Wrist
Landmarks 1-4: Thumb
Landmarks 5-8: Index finger (tip at 8)
Landmarks 9-12: Middle finger
Landmarks 13-16: Ring finger
Landmarks 17-20: Pinky

Performance

Target FPS: 30+
Resolution: 1280x720 (configurable)
Detection Confidence: 0.7
Tracking Confidence: 0.5

Configuration
Edit src/utils/config.py to customize:
python# Camera settings
CAMERA_INDEX = 0              # Change for different camera
FRAME_WIDTH = 1280            # Resolution width
FRAME_HEIGHT = 720            # Resolution height

# Detection settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1

# Display settings
SHOW_FPS = True
Troubleshooting
Camera Not Found

Check CAMERA_INDEX in config.py
Try values 0, 1, 2 for different cameras
Ensure camera is not being used by another application

Low FPS

Reduce resolution in config.py
Close other applications
Check CPU usage

Hand Not Detected

Ensure good lighting
Keep hand clearly visible
Adjust detection confidence if needed

Next Steps (Phase 2)
Phase 2 will implement:

Gesture recognition logic
Start/stop writing gestures
Space and clear canvas gestures
Real-time gesture feedback

Dependencies

opencv-python: Camera capture and image processing
mediapipe: Hand detection and landmark tracking
numpy: Numerical operations