import cv2
import mediapipe as mp

class LandmarkUtils:
    """Utilities for working with hand landmarks"""
    
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        
    def draw_landmarks(self, image, hand_landmarks):
        """
        Draw hand landmarks and connections on the image
        
        Args:
            image: OpenCV image (BGR)
            hand_landmarks: MediaPipe hand landmarks
        """
        self.mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
        
    def get_landmark_position(self, hand_landmarks, landmark_id, frame_width, frame_height):
        """
        Get pixel coordinates of a specific landmark
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            landmark_id: ID of the landmark to retrieve
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            tuple: (x, y) pixel coordinates
        """
        if hand_landmarks is None:
            return None
            
        landmark = hand_landmarks.landmark[landmark_id]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        
        return (x, y)
        
    def draw_fingertip_indicator(self, image, position, color=(0, 255, 255), radius=10):
        """
        Draw a circle indicator at the fingertip position
        
        Args:
            image: OpenCV image
            position: (x, y) coordinates
            color: BGR color tuple
            radius: Circle radius
        """
        if position is not None:
            cv2.circle(image, position, radius, color, -1)
            cv2.circle(image, position, radius + 5, color, 2)