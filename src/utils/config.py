# Configuration settings for the air-writing application - Phase 3

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS_TARGET = 30

# Hand detection settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1

# Display settings
WINDOW_NAME = "Air Writing - Phase 3: Stroke Smoothing"
LANDMARK_DRAW_SPEC_COLOR = (0, 255, 0)  # Green
LANDMARK_DRAW_SPEC_THICKNESS = 2
CONNECTION_DRAW_SPEC_COLOR = (255, 0, 0)  # Blue
CONNECTION_DRAW_SPEC_THICKNESS = 2

# Index finger tip landmark ID (MediaPipe hand landmark)
INDEX_FINGER_TIP = 8

# Gesture settings
GESTURE_HOLD_FRAMES = 5  # Frames to hold gesture before confirming
MIN_DISTANCE_THRESHOLD = 5  # Minimum pixel distance to add stroke point

# Smoothing settings (Phase 3)
ENABLE_SMOOTHING = True
DEFAULT_SMOOTHING_METHOD = 'savitzky_golay'  # Best default
REAL_TIME_SMOOTHING = True  # Apply smoothing during writing

# Smoothing method parameters
MOVING_AVERAGE_WINDOW = 5
GAUSSIAN_SIGMA = 2.0
SAVGOL_WINDOW = 11
SAVGOL_POLYORDER = 3
SPLINE_SMOOTHING_FACTOR = 0.0
KALMAN_PROCESS_VAR = 1e-5
KALMAN_MEASUREMENT_VAR = 1e-1

# Performance settings
SHOW_FPS = True

# UI settings
SHOW_GESTURE_GUIDE = True
SHOW_RAW_STROKE_OVERLAY = False