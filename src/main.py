import cv2
import time
import sys
from src.camera.camera_stream import CameraStream
from src.hand_tracking.hand_detector import HandDetector
from src.hand_tracking.landmark_utils import LandmarkUtils
from src.utils.config import *

class AirWritingApp:
    """Main application for Phase 1: Hand Detection & Tracking"""
    
    def __init__(self):
        """Initialize the application"""
        print("="*60)
        print("AIR WRITING APPLICATION - PHASE 1")
        print("Hand Detection & Tracking")
        print("="*60)
        
        # Initialize components
        self.camera = CameraStream(CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT)
        self.hand_detector = HandDetector(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=MAX_NUM_HANDS
        )
        self.landmark_utils = LandmarkUtils()
        
        # FPS calculation
        self.prev_time = 0
        self.fps = 0
        
        print(f"\nConfiguration:")
        print(f"  - Camera Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
        print(f"  - Detection Confidence: {MIN_DETECTION_CONFIDENCE}")
        print(f"  - Tracking Confidence: {MIN_TRACKING_CONFIDENCE}")
        print(f"  - Max Hands: {MAX_NUM_HANDS}")
        print("\nControls:")
        print("  - Press 'q' or 'ESC' to quit")
        print("="*60)
        
    def calculate_fps(self):
        """Calculate current FPS"""
        current_time = time.time()
        self.fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        
    def draw_ui(self, frame, hand_detected, finger_tip_pos):
        """
        Draw UI elements on the frame
        
        Args:
            frame: OpenCV image
            hand_detected: Boolean indicating if hand is detected
            finger_tip_pos: (x, y) position of index finger tip or None
        """
        height, width = frame.shape[:2]
        
        # Draw FPS
        if SHOW_FPS:
            fps_text = f"FPS: {int(self.fps)}"
            cv2.putText(frame, fps_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw hand detection status
        status_text = "Hand Detected" if hand_detected else "No Hand Detected"
        status_color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.putText(frame, status_text, (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Draw index finger tip indicator
        if finger_tip_pos:
            self.landmark_utils.draw_fingertip_indicator(
                frame, finger_tip_pos, color=(0, 255, 255), radius=10
            )
            
            # Draw coordinates
            coord_text = f"Index Tip: ({finger_tip_pos[0]}, {finger_tip_pos[1]})"
            cv2.putText(frame, coord_text, (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Draw instructions
        cv2.putText(frame, "Press 'q' or 'ESC' to quit", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
    def run(self):
        """Main application loop"""
        # Start camera
        self.camera.start()
        
        # Initialize time for FPS calculation
        self.prev_time = time.time()
        
        print("\n[INFO] Starting hand tracking... Show your hand to the camera!")
        
        try:
            while True:
                # Read frame from camera
                success, frame = self.camera.read_frame()
                
                if not success:
                    print("[ERROR] Failed to read frame from camera")
                    break
                
                # Detect hands
                hand_detected = self.hand_detector.detect(frame)
                
                # Get index finger tip position
                finger_tip_pos = None
                if hand_detected:
                    height, width = frame.shape[:2]
                    finger_tip_pos = self.hand_detector.get_index_finger_tip(width, height)
                    
                    # Draw hand landmarks
                    self.hand_detector.draw_landmarks(frame)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Draw UI elements
                self.draw_ui(frame, hand_detected, finger_tip_pos)
                
                # Display the frame
                cv2.imshow(WINDOW_NAME, frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    print("\n[INFO] Exiting application...")
                    break
                    
        except KeyboardInterrupt:
            print("\n[INFO] Application interrupted by user")
            
        finally:
            # Cleanup
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        self.hand_detector.close()
        self.camera.release()
        cv2.destroyAllWindows()
        print("[INFO] Cleanup completed")

def main():
    """Entry point"""
    app = AirWritingApp()
    app.run()

if __name__ == "__main__":
    main()