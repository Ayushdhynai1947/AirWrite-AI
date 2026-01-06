import cv2
import sys

class CameraStream:
    """Handles camera initialization and frame capture"""
    
    def __init__(self, camera_index=0, width=1280, height=720):
        """
        Initialize camera stream
        
        Args:
            camera_index: Camera device index (default: 0)
            width: Frame width
            height: Frame height
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        
    def start(self):
        """Start the camera stream"""
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Error: Cannot open camera at index {self.camera_index}")
            sys.exit(1)
            
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        print(f"Camera started: {self.width}x{self.height}")
        
    def read_frame(self):
        """
        Read a frame from the camera
        
        Returns:
            tuple: (success, frame)
        """
        if self.cap is None:
            return False, None
            
        success, frame = self.cap.read()
        
        if success:
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
        return success, frame
        
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            print("Camera released")
            
    def __del__(self):
        """Cleanup on object destruction"""
        self.release()