# Configuration settings for the air-writing application

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS_TARGET = 30

# Hand detection settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 2

# Display settings
WINDOW_NAME = "Air Writing - Hand Tracking"
LANDMARK_DRAW_SPEC_COLOR = (0, 255, 0)  # Green
LANDMARK_DRAW_SPEC_THICKNESS = 2
CONNECTION_DRAW_SPEC_COLOR = (255, 0, 0)  # Blue
CONNECTION_DRAW_SPEC_THICKNESS = 2

# Index finger tip landmark ID (MediaPipe hand landmark)
INDEX_FINGER_TIP = 8

# Performance settings
SHOW_FPS = True