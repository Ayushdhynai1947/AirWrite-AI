import cv2
import mediapipe as mp
from src.hand_tracking.landmark_utils import LandmarkUtils

class HandDetector:
    """Real-time hand detection and tracking using MediaPipe"""
    
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1):
        """
        Initialize hand detector
        
        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
            max_num_hands: Maximum number of hands to detect
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.landmark_utils = LandmarkUtils()
        self.results = None
        
    def detect(self, frame):
        """
        Detect hands in the frame
        
        Args:
            frame: OpenCV BGR image
            
        Returns:
            bool: True if hand(s) detected, False otherwise
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        self.results = self.hands.process(rgb_frame)
        
        return self.results.multi_hand_landmarks is not None
        
    def get_hand_landmarks(self):
        """
        Get detected hand landmarks
        
        Returns:
            Hand landmarks or None if no hands detected
        """
        if self.results and self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks[0]
        return None
        
    def draw_landmarks(self, frame):
        """
        Draw hand landmarks on the frame
        
        Args:
            frame: OpenCV image to draw on
        """
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.landmark_utils.draw_landmarks(frame, hand_landmarks)
                
    def get_index_finger_tip(self, frame_width, frame_height, landmark_id=8):
        """
        Get the position of the index finger tip
        
        Args:
            frame_width: Width of the frame
            frame_height: Height of the frame
            landmark_id: Landmark ID (default: 8 for index finger tip)
            
        Returns:
            tuple: (x, y) coordinates or None
        """
        hand_landmarks = self.get_hand_landmarks()
        
        if hand_landmarks:
            return self.landmark_utils.get_landmark_position(
                hand_landmarks, 
                landmark_id, 
                frame_width, 
                frame_height
            )
        return None
        
    def close(self):
        """Release MediaPipe resources"""
        if self.hands:
            self.hands.close()