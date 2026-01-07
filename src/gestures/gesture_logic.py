import math
import numpy as np

class GestureRecognizer:
    """Recognizes hand gestures for air writing control"""
    
    # Gesture states
    GESTURE_NONE = "none"
    GESTURE_WRITING = "writing"  # Index finger up
    GESTURE_STOP = "stop"  # Fist closed
    GESTURE_SPACE = "space"  # Two fingers up (index + middle)
    GESTURE_CLEAR = "clear"  # Thumb + index pinch
    
    def __init__(self, gesture_hold_frames=5):
        """
        Initialize gesture recognizer
        
        Args:
            gesture_hold_frames: Number of frames to hold gesture before confirming
        """
        self.current_gesture = self.GESTURE_NONE
        self.previous_gesture = self.GESTURE_NONE
        self.gesture_hold_frames = gesture_hold_frames
        self.gesture_frame_count = 0
        self.confirmed_gesture = self.GESTURE_NONE
        
        # MediaPipe landmark indices
        self.WRIST = 0
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.INDEX_MCP = 5
        self.MIDDLE_TIP = 12
        self.MIDDLE_MCP = 9
        self.RING_TIP = 16
        self.RING_MCP = 13
        self.PINKY_TIP = 20
        self.PINKY_MCP = 17
        
    def get_landmark_coords(self, hand_landmarks, landmark_id, frame_width, frame_height):
        """Get normalized and pixel coordinates of a landmark"""
        landmark = hand_landmarks.landmark[landmark_id]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        return (x, y), (landmark.x, landmark.y, landmark.z)
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        
    def is_finger_extended(self, hand_landmarks, tip_id, mcp_id, wrist_coords):
        """Check if a finger is extended"""
        tip = hand_landmarks.landmark[tip_id]
        mcp = hand_landmarks.landmark[mcp_id]
        
        # Finger is extended if tip is above MCP joint (lower y value)
        # and further from wrist
        tip_to_wrist = self.calculate_distance(
            (tip.x, tip.y), (wrist_coords[0], wrist_coords[1])
        )
        mcp_to_wrist = self.calculate_distance(
            (mcp.x, mcp.y), (wrist_coords[0], wrist_coords[1])
        )
        
        return tip_to_wrist > mcp_to_wrist * 0.9
        
    def is_thumb_extended(self, hand_landmarks):
        """Check if thumb is extended"""
        thumb_tip = hand_landmarks.landmark[self.THUMB_TIP]
        index_mcp = hand_landmarks.landmark[self.INDEX_MCP]
        
        # Thumb is extended if it's far from index finger base
        distance = self.calculate_distance(
            (thumb_tip.x, thumb_tip.y),
            (index_mcp.x, index_mcp.y)
        )
        
        return distance > 0.1
        
    def detect_gesture(self, hand_landmarks, frame_width, frame_height):
        """
        Detect current gesture from hand landmarks
        
        Returns:
            str: Detected gesture name
        """
        if hand_landmarks is None:
            return self.GESTURE_NONE
            
        # Get key landmarks
        wrist = hand_landmarks.landmark[self.WRIST]
        wrist_norm = (wrist.x, wrist.y, wrist.z)
        
        thumb_tip_px, thumb_tip = self.get_landmark_coords(
            hand_landmarks, self.THUMB_TIP, frame_width, frame_height
        )
        index_tip_px, index_tip = self.get_landmark_coords(
            hand_landmarks, self.INDEX_TIP, frame_width, frame_height
        )
        
        # Check finger states
        index_extended = self.is_finger_extended(
            hand_landmarks, self.INDEX_TIP, self.INDEX_MCP, wrist_norm
        )
        middle_extended = self.is_finger_extended(
            hand_landmarks, self.MIDDLE_TIP, self.MIDDLE_MCP, wrist_norm
        )
        ring_extended = self.is_finger_extended(
            hand_landmarks, self.RING_TIP, self.RING_MCP, wrist_norm
        )
        pinky_extended = self.is_finger_extended(
            hand_landmarks, self.PINKY_TIP, self.PINKY_MCP, wrist_norm
        )
        thumb_extended = self.is_thumb_extended(hand_landmarks)
        
        # Count extended fingers
        extended_count = sum([
            index_extended, middle_extended, ring_extended, pinky_extended
        ])
        
        # Gesture 1: CLEAR - Thumb and index pinch (close together)
        thumb_index_distance = self.calculate_distance(
            (thumb_tip[0], thumb_tip[1]),
            (index_tip[0], index_tip[1])
        )
        if thumb_index_distance < 0.05 and not ring_extended and not pinky_extended:
            return self.GESTURE_CLEAR
            
        # Gesture 2: SPACE - Two fingers up (index + middle)
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            return self.GESTURE_SPACE
            
        # Gesture 3: WRITING - Only index finger up
        if index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return self.GESTURE_WRITING
            
        # Gesture 4: STOP - Fist (no fingers extended)
        if extended_count == 0 and not thumb_extended:
            return self.GESTURE_STOP
            
        return self.GESTURE_NONE
        
    def update_gesture(self, hand_landmarks, frame_width, frame_height):
        """
        Update gesture state with temporal smoothing
        
        Returns:
            tuple: (current_gesture, gesture_changed)
        """
        detected_gesture = self.detect_gesture(hand_landmarks, frame_width, frame_height)
        
        # Temporal smoothing - require gesture to be held for multiple frames
        if detected_gesture == self.current_gesture:
            self.gesture_frame_count += 1
        else:
            self.current_gesture = detected_gesture
            self.gesture_frame_count = 1
            
        # Confirm gesture if held long enough
        gesture_changed = False
        if self.gesture_frame_count >= self.gesture_hold_frames:
            if self.confirmed_gesture != self.current_gesture:
                self.previous_gesture = self.confirmed_gesture
                self.confirmed_gesture = self.current_gesture
                gesture_changed = True
                
        return self.confirmed_gesture, gesture_changed
        
    def get_gesture_info(self):
        """Get current gesture information"""
        return {
            'gesture': self.confirmed_gesture,
            'previous': self.previous_gesture,
            'confidence': min(self.gesture_frame_count / self.gesture_hold_frames, 1.0)
        }
        
    def is_writing_active(self):
        """Check if writing mode is active"""
        return self.confirmed_gesture == self.GESTURE_WRITING
        
    def reset(self):
        """Reset gesture state"""
        self.current_gesture = self.GESTURE_NONE
        self.confirmed_gesture = self.GESTURE_NONE
        self.previous_gesture = self.GESTURE_NONE
        self.gesture_frame_count = 0