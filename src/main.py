# import cv2
# import time
# import sys
# from src.camera.camera_stream import CameraStream
# from src.hand_tracking.hand_detector import HandDetector
# from src.hand_tracking.landmark_utils import LandmarkUtils
# from src.gestures.gesture_logic import GestureRecognizer
# from src.strokes.stroke_tracker import StrokeTracker
# from src.ui.display import DisplayUI
# from src.utils.config import *

# class AirWritingApp:
#     """Main application for Phase 1: Hand Detection & Tracking"""
    
#     def __init__(self):
#         """Initialize the application"""
#         print("="*60)
#         print("AIR WRITING APPLICATION - PHASE 1")
#         print("Hand Detection & Tracking")
#         print("="*60)
        
#         # Initialize components
#         self.camera = CameraStream(CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT)
#         self.hand_detector = HandDetector(
#             min_detection_confidence=MIN_DETECTION_CONFIDENCE,
#             min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
#             max_num_hands=MAX_NUM_HANDS
#         )
#         self.landmark_utils = LandmarkUtils()
        
#         # Phase 2 components
#         self.gesture_recognizer = GestureRecognizer(gesture_hold_frames=5)
#         self.stroke_tracker = StrokeTracker(min_distance_threshold=5)
#         self.display_ui = DisplayUI()
        
#         # State management
#         self.is_writing = False
#         self.show_gesture_feedback = False
#         self.feedback_start_time = 0
#         self.feedback_gesture = None
#         self.space_count = 0
        
        
#         # FPS calculation
#         self.prev_time = 0
#         self.fps = 0
        
#         print(f"\nConfiguration:")
#         print(f"  - Camera Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
#         print(f"  - Detection Confidence: {MIN_DETECTION_CONFIDENCE}")
#         print(f"  - Tracking Confidence: {MIN_TRACKING_CONFIDENCE}")
#         print(f"  - Max Hands: {MAX_NUM_HANDS}")
        
#         print("\n📝 Gesture Controls:")
#         print("  ☝️  Index finger up    → START WRITING")
#         print("  ✊  Fist closed        → STOP WRITING")
#         print("  ✌️  Two fingers up     → ADD SPACE")
#         print("  🤏  Thumb + Index pinch → CLEAR CANVAS")
        
#         print("\n⌨️  Keyboard Controls:")
#         print("  - Press 'q' or 'ESC' to quit")
#         print("  - Press 'c' to clear canvas")
#         print("  - Press 'h' to toggle gesture guide")
#         print("="*60)
        
#         self.show_guide = True
#     def calculate_fps(self):
#         """Calculate current FPS"""
#         current_time = time.time()
#         self.fps = 1 / (current_time - self.prev_time)
#         self.prev_time = current_time
        
#     def trigger_feedback(self, gesture):
#         """Trigger visual feedback for a gesture"""
#         self.show_gesture_feedback = True
#         self.feedback_start_time = time.time()
#         self.feedback_gesture = gesture
        
#     def handle_gesture_actions(self, gesture, gesture_changed, finger_tip_pos):
#         """
#         Handle gesture-based actions
        
#         Args:
#             gesture: Current confirmed gesture
#             gesture_changed: Boolean if gesture just changed
#             finger_tip_pos: (x, y) position of index finger tip
#         """
#         # Only act on gesture changes
#         if not gesture_changed:
#             return
            
#         if gesture == GestureRecognizer.GESTURE_WRITING:
#             # Start writing
#             if not self.is_writing and finger_tip_pos:
#                 self.is_writing = True
#                 self.stroke_tracker.start_stroke(finger_tip_pos)
#                 self.trigger_feedback('writing')
#                 print("[GESTURE] Writing started")
                
#         elif gesture == GestureRecognizer.GESTURE_STOP:
#             # Stop writing
#             if self.is_writing:
#                 self.is_writing = False
#                 completed_stroke = self.stroke_tracker.end_stroke()
#                 if completed_stroke:
#                     print(f"[GESTURE] Stroke completed: {len(completed_stroke)} points")
#                 self.trigger_feedback('stop')
#                 print("[GESTURE] Writing stopped")
                
#         elif gesture == GestureRecognizer.GESTURE_SPACE:
#             # Add space (we'll implement this more in later phases)
#             self.space_count += 1
#             self.trigger_feedback('space')
#             print(f"[GESTURE] Space added (total: {self.space_count})")
            
#         elif gesture == GestureRecognizer.GESTURE_CLEAR:
#             # Clear canvas
#             self.stroke_tracker.clear_all_strokes()
#             self.is_writing = False
#             self.space_count = 0
#             self.trigger_feedback('clear')
#             print("[GESTURE] Canvas cleared")
        
        
#     def draw_ui(self, frame, hand_detected, finger_tip_pos , gesture_info):
#         """
#         Draw UI elements on the frame
        
#         Args:
#             frame: OpenCV image
#             hand_detected: Boolean indicating if hand is detected
#             finger_tip_pos: (x, y) position of index finger tip or None
#             gesture_info: Gesture information dictionary
#         """
#         height, width = frame.shape[:2]
        
#         # Draw FPS
#         if SHOW_FPS:
#             fps_text = f"FPS: {int(self.fps)}"
#             cv2.putText(frame, fps_text, (10, 30), 
#                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
#         # Draw hand detection status
#         status_text = "Hand Detected" if hand_detected else "No Hand Detected"
#         status_color = (0, 255, 0) if hand_detected else (0, 0, 255)
#         cv2.putText(frame, status_text, (10, 70), 
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
#         # Draw index finger tip indicator
#         if finger_tip_pos:
#             self.landmark_utils.draw_fingertip_indicator(
#                 frame, finger_tip_pos, color=(0, 255, 255), radius=10
#             )
            
#             # Draw coordinates
#             coord_text = f"Index Tip: ({finger_tip_pos[0]}, {finger_tip_pos[1]})"
#             cv2.putText(frame, coord_text, (10, 110), 
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
#         # Draw instructions
#         cv2.putText(frame, "Press 'q' or 'ESC' to quit", (10, height - 20), 
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
#     def run(self):
#         """Main application loop"""
#         # Start camera
#         self.camera.start()
        
#         # Initialize time for FPS calculation
#         self.prev_time = time.time()
        
#         print("\n[INFO] Starting hand tracking... Show your hand to the camera!")
        
#         try:
#             while True:
#                 # Read frame from camera
#                 success, frame = self.camera.read_frame()
                
#                 if not success:
#                     print("[ERROR] Failed to read frame from camera")
#                     break
                
#                 # Detect hands
#                 hand_detected = self.hand_detector.detect(frame)
                
#                 # Get index finger tip position
#                 finger_tip_pos = None
#                 if hand_detected:
#                     height, width = frame.shape[:2]
#                     finger_tip_pos = self.hand_detector.get_index_finger_tip(width, height)
                    
#                     # Draw hand landmarks
#                     self.hand_detector.draw_landmarks(frame)
                
#                 # Calculate FPS
#                 self.calculate_fps()
                
#                 # Draw UI elements
#                 self.draw_ui(frame, hand_detected, finger_tip_pos)
                
#                 # Display the frame
#                 cv2.imshow(WINDOW_NAME, frame)
                
#                 # Handle key presses
#                 key = cv2.waitKey(1) & 0xFF
#                 if key == ord('q') or key == 27:  # 'q' or ESC
#                     print("\n[INFO] Exiting application...")
#                     break
                    
#         except KeyboardInterrupt:
#             print("\n[INFO] Application interrupted by user")
            
#         finally:
#             # Cleanup
#             self.cleanup()
            
#     def cleanup(self):
#         """Clean up resources"""
#         self.hand_detector.close()
#         self.camera.release()
#         cv2.destroyAllWindows()
#         print("[INFO] Cleanup completed")

# def main():
#     """Entry point"""
#     app = AirWritingApp()
#     app.run()

# if __name__ == "__main__":
#     main()

import cv2
import time
import sys
from src.camera.camera_stream import CameraStream
from src.hand_tracking.hand_detector import HandDetector
from src.hand_tracking.landmark_utils import LandmarkUtils
from src.gestures.gesture_logic import GestureRecognizer
from src.strokes.stroke_tracker import StrokeTracker
from src.ui.display import DisplayUI
from src.utils.config import *

class AirWritingApp:
    """Main application for Air Writing - Phase 2: Gesture Logic & Writing Control"""
    
    def __init__(self):
        """Initialize the application"""
        print("="*60)
        print("AIR WRITING APPLICATION - PHASE 2")
        print("Gesture Logic & Writing Control")
        print("="*60)
        
        # Initialize components
        self.camera = CameraStream(CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT)
        self.hand_detector = HandDetector(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=MAX_NUM_HANDS
        )
        self.landmark_utils = LandmarkUtils()
        
        # Phase 2 components
        self.gesture_recognizer = GestureRecognizer(gesture_hold_frames=5)
        self.stroke_tracker = StrokeTracker(min_distance_threshold=5)
        self.display_ui = DisplayUI()
        
        # State management
        self.is_writing = False
        self.show_gesture_feedback = False
        self.feedback_start_time = 0
        self.feedback_gesture = None
        self.space_count = 0
        
        # FPS calculation
        self.prev_time = 0
        self.fps = 0
        
        print(f"\nConfiguration:")
        print(f"  - Camera Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
        print(f"  - Detection Confidence: {MIN_DETECTION_CONFIDENCE}")
        print(f"  - Tracking Confidence: {MIN_TRACKING_CONFIDENCE}")
        print(f"  - Max Hands: {MAX_NUM_HANDS}")
        
        print("\n📝 Gesture Controls:")
        print("  ☝️  Index finger up    → START WRITING")
        print("  ✊  Fist closed        → STOP WRITING")
        print("  ✌️  Two fingers up     → ADD SPACE")
        print("  🤏  Thumb + Index pinch → CLEAR CANVAS")
        
        print("\n⌨️  Keyboard Controls:")
        print("  - Press 'q' or 'ESC' to quit")
        print("  - Press 'c' to clear canvas")
        print("  - Press 'h' to toggle gesture guide")
        print("="*60)
        
        self.show_guide = True
        
    def calculate_fps(self):
        """Calculate current FPS"""
        current_time = time.time()
        self.fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        
    def trigger_feedback(self, gesture):
        """Trigger visual feedback for a gesture"""
        self.show_gesture_feedback = True
        self.feedback_start_time = time.time()
        self.feedback_gesture = gesture
        
    def handle_gesture_actions(self, gesture, gesture_changed, finger_tip_pos):
        """
        Handle gesture-based actions
        
        Args:
            gesture: Current confirmed gesture
            gesture_changed: Boolean if gesture just changed
            finger_tip_pos: (x, y) position of index finger tip
        """
        # Only act on gesture changes
        if not gesture_changed:
            return
            
        if gesture == GestureRecognizer.GESTURE_WRITING:
            # Start writing
            if not self.is_writing and finger_tip_pos:
                self.is_writing = True
                self.stroke_tracker.start_stroke(finger_tip_pos)
                self.trigger_feedback('writing')
                print("[GESTURE] Writing started")
                
        elif gesture == GestureRecognizer.GESTURE_STOP:
            # Stop writing
            if self.is_writing:
                self.is_writing = False
                completed_stroke = self.stroke_tracker.end_stroke()
                if completed_stroke:
                    print(f"[GESTURE] Stroke completed: {len(completed_stroke)} points")
                self.trigger_feedback('stop')
                print("[GESTURE] Writing stopped")
                
        elif gesture == GestureRecognizer.GESTURE_SPACE:
            # Add space (we'll implement this more in later phases)
            self.space_count += 1
            self.trigger_feedback('space')
            print(f"[GESTURE] Space added (total: {self.space_count})")
            
        elif gesture == GestureRecognizer.GESTURE_CLEAR:
            # Clear canvas
            self.stroke_tracker.clear_all_strokes()
            self.is_writing = False
            self.space_count = 0
            self.trigger_feedback('clear')
            print("[GESTURE] Canvas cleared")
            
    def draw_ui(self, frame, hand_detected, finger_tip_pos, gesture_info):
        """
        Draw all UI elements
        
        Args:
            frame: OpenCV image
            hand_detected: Boolean indicating if hand is detected
            finger_tip_pos: (x, y) position of index finger tip or None
            gesture_info: Gesture information dictionary
        """
        # Draw FPS
        if SHOW_FPS:
            self.display_ui.draw_fps(frame, self.fps)
        
        # Draw gesture indicator
        self.display_ui.draw_gesture_indicator(frame, gesture_info, position=(10, 70))
        
        # Draw all completed strokes
        self.display_ui.draw_all_strokes(frame, self.stroke_tracker.get_all_strokes())
        
        # Draw current stroke being drawn
        if self.is_writing:
            current_stroke = self.stroke_tracker.get_current_stroke()
            self.display_ui.draw_stroke_preview(frame, current_stroke)
            
            # Draw fingertip indicator when writing
            if finger_tip_pos:
                self.landmark_utils.draw_fingertip_indicator(
                    frame, finger_tip_pos, color=(0, 255, 255), radius=8
                )
        
        # Draw statistics
        stroke_count = self.stroke_tracker.get_stroke_count()
        self.display_ui.draw_stats(frame, stroke_count)
        
        # Draw gesture guide
        if self.show_guide:
            height = frame.shape[0]
            self.display_ui.draw_gesture_guide(frame, position=(10, height - 150))
        
        # Draw gesture feedback
        if self.show_gesture_feedback:
            if time.time() - self.feedback_start_time < 1.0:
                self.display_ui.show_gesture_feedback(frame, self.feedback_gesture)
            else:
                self.show_gesture_feedback = False
        
        # Draw instructions
        height, width = frame.shape[:2]
        instructions = "Press 'h' for help | 'c' to clear | 'q' to quit"
        cv2.putText(frame, instructions, (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
    def run(self):
        """Main application loop"""
        # Start camera
        self.camera.start()
        
        # Initialize time for FPS calculation
        self.prev_time = time.time()
        
        print("\n[INFO] Application started! Show your hand to the camera.")
        print("[INFO] Make gestures to control air writing...\n")
        
        try:
            while True:
                # Read frame from camera
                success, frame = self.camera.read_frame()
                
                if not success:
                    print("[ERROR] Failed to read frame from camera")
                    break
                
                height, width = frame.shape[:2]
                
                # Detect hands
                hand_detected = self.hand_detector.detect(frame)
                
                # Get index finger tip position
                finger_tip_pos = None
                gesture_info = self.gesture_recognizer.get_gesture_info()
                
                if hand_detected:
                    # Get hand landmarks
                    hand_landmarks = self.hand_detector.get_hand_landmarks()
                    
                    # Get index finger tip position
                    finger_tip_pos = self.hand_detector.get_index_finger_tip(width, height)
                    
                    # Update gesture recognition
                    gesture, gesture_changed = self.gesture_recognizer.update_gesture(
                        hand_landmarks, width, height
                    )
                    gesture_info = self.gesture_recognizer.get_gesture_info()
                    
                    # Handle gesture actions
                    self.handle_gesture_actions(gesture, gesture_changed, finger_tip_pos)
                    
                    # If writing, track the stroke
                    if self.is_writing and finger_tip_pos:
                        self.stroke_tracker.add_point(finger_tip_pos)
                    
                    # Draw hand landmarks (lighter when not writing)
                    if not self.is_writing:
                        self.hand_detector.draw_landmarks(frame)
                else:
                    # No hand detected - stop writing if active
                    if self.is_writing:
                        self.is_writing = False
                        self.stroke_tracker.end_stroke()
                    
                    # Reset gesture recognizer
                    self.gesture_recognizer.reset()
                
                # Calculate FPS
                self.calculate_fps()
                
                # Draw all UI elements
                self.draw_ui(frame, hand_detected, finger_tip_pos, gesture_info)
                
                # Display the frame
                cv2.imshow(WINDOW_NAME, frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    print("\n[INFO] Exiting application...")
                    break
                elif key == ord('c'):  # Clear canvas
                    self.stroke_tracker.clear_all_strokes()
                    self.space_count = 0
                    print("[INFO] Canvas cleared (keyboard)")
                elif key == ord('h'):  # Toggle help
                    self.show_guide = not self.show_guide
                    print(f"[INFO] Gesture guide: {'ON' if self.show_guide else 'OFF'}")
                    
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
        
        # Print session summary
        print("\n" + "="*60)
        print("SESSION SUMMARY")
        print("="*60)
        print(f"  Total Strokes: {self.stroke_tracker.get_stroke_count()}")
        print(f"  Spaces Added: {self.space_count}")
        print("="*60)
        print("[INFO] Cleanup completed")

def main():
    """Entry point"""
    app = AirWritingApp()
    app.run()

if __name__ == "__main__":
    main()