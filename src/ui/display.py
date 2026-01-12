import cv2
import numpy as np

class DisplayUI:
    """Handles UI rendering and visual feedback"""
    
    def __init__(self):
        """Initialize display UI"""
        self.colors = {
            'writing': (0, 255, 0),      # Green
            'stop': (0, 0, 255),          # Red
            'space': (255, 165, 0),       # Orange
            'clear': (255, 0, 255),       # Magenta
            'none': (128, 128, 128),      # Gray
            'stroke': (0, 255, 255),      # Yellow (Cyan)
            'completed': (255, 255, 0)    # Cyan (Yellow)
        }
        
    def draw_gesture_indicator(self, frame, gesture_info, position=(10, 100)):
        """
        Draw gesture status indicator
        
        Args:
            frame: OpenCV image
            gesture_info: Dictionary with gesture information
            position: (x, y) position to draw
        """
        x, y = position
        gesture = gesture_info['gesture']
        confidence = gesture_info.get('confidence', 1.0)
        
        # Map gesture to display text
        gesture_text_map = {
            'writing': '✍️  WRITING',
            'stop': '✋ STOP',
            'space': '✌️  SPACE',
            'clear': '🧹 CLEAR',
            'none': '👋 NO GESTURE'
        }
        
        text = gesture_text_map.get(gesture, gesture.upper())
        color = self.colors.get(gesture, self.colors['none'])
        
        # Draw background rectangle
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        cv2.rectangle(frame, (x - 5, y - text_size[1] - 10), 
                     (x + text_size[0] + 10, y + 5), (0, 0, 0), -1)
        cv2.rectangle(frame, (x - 5, y - text_size[1] - 10), 
                     (x + text_size[0] + 10, y + 5), color, 2)
        
        # Draw text
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, color, 2)
        
        # Draw confidence bar
        if confidence < 1.0:
            bar_width = int((text_size[0] + 15) * confidence)
            cv2.rectangle(frame, (x - 5, y + 10), 
                         (x - 5 + bar_width, y + 15), color, -1)
            
    def draw_stroke_preview(self, frame, current_stroke, raw_stroke=None, color=None, show_raw=False):
        """
        Draw current stroke being written with optional raw overlay
        
        Args:
            frame: OpenCV image
            current_stroke: List of (x, y) smoothed points
            raw_stroke: List of (x, y) raw points (optional)
            color: Stroke color (default: yellow)
            show_raw: Show raw stroke overlay
        """
        if color is None:
            color = self.colors['stroke']
        
        # Draw raw stroke if requested (lighter color)
        if show_raw and raw_stroke and len(raw_stroke) >= 2:
            raw_color = (180, 180, 180)  # Light gray
            for i in range(1, len(raw_stroke)):
                cv2.line(frame, raw_stroke[i-1], raw_stroke[i], 
                        raw_color, 1, cv2.LINE_AA)
            
        # Draw smoothed stroke
        if len(current_stroke) < 2:
            return
            
        # Draw line connecting all points
        for i in range(1, len(current_stroke)):
            cv2.line(frame, current_stroke[i-1], current_stroke[i], 
                    color, 3, cv2.LINE_AA)
            
        # Draw circles at each point for smoothness indicator
        for point in current_stroke[::2]:  # Draw every other point
            cv2.circle(frame, point, 2, color, -1)
            
    def draw_all_strokes(self, frame, all_strokes, color=None):
        """
        Draw all completed strokes
        
        Args:
            frame: OpenCV image
            all_strokes: List of stroke dictionaries
            color: Stroke color (default: cyan)
        """
        if color is None:
            color = self.colors['completed']
            
        for stroke_data in all_strokes:
            points = stroke_data['points']
            if len(points) < 2:
                continue
                
            # Draw stroke
            for i in range(1, len(points)):
                cv2.line(frame, points[i-1], points[i], 
                        color, 3, cv2.LINE_AA)
                        
    def draw_canvas_overlay(self, frame, alpha=0.3):
        """
        Draw semi-transparent canvas overlay for writing area
        
        Args:
            frame: OpenCV image
            alpha: Transparency level (0-1)
        """
        height, width = frame.shape[:2]
        overlay = frame.copy()
        
        # Draw writing area rectangle
        cv2.rectangle(overlay, (50, 150), (width - 50, height - 50), 
                     (255, 255, 255), 2)
        
        # Blend with original
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
    def draw_gesture_guide(self, frame, position=(10, 150)):
        """
        Draw gesture guide/help
        
        Args:
            frame: OpenCV image
            position: Starting (x, y) position
        """
        x, y = position
        guides = [
            ("☝️  Index up: Write", self.colors['writing']),
            ("✊ Fist: Stop", self.colors['stop']),
            ("✌️  Two fingers: Space", self.colors['space']),
            ("🤏 Pinch: Clear", self.colors['clear']),
            ("", (0, 0, 0)),
            ("Press 's': Toggle smooth", (150, 150, 150)),
            ("Press 'r': Show raw", (150, 150, 150))
        ]
        
        line_height = 25
        for i, (text, color) in enumerate(guides):
            if text:
                y_pos = y + (i * line_height)
                cv2.putText(frame, text, (x, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
                       
    def draw_stats(self, frame, stroke_count, smoothing_enabled=None, smoothing_method=None, position=None):
        """
        Draw statistics
        
        Args:
            frame: OpenCV image
            stroke_count: Number of completed strokes
            smoothing_enabled: Whether smoothing is enabled
            smoothing_method: Current smoothing method
            position: (x, y) position
        """
        if position is None:
            height, width = frame.shape[:2]
            position = (width - 300, 30)
            
        x, y = position
        
        # Draw stats background
        cv2.rectangle(frame, (x - 10, y - 25), (x + 290, y + 65), (0, 0, 0), -1)
        cv2.rectangle(frame, (x - 10, y - 25), (x + 290, y + 65), (100, 100, 100), 2)
        
        # Stroke count
        stats_text = f"Strokes: {stroke_count}"
        cv2.putText(frame, stats_text, (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Smoothing status
        if smoothing_enabled is not None:
            y += 25
            smooth_status = "ON" if smoothing_enabled else "OFF"
            smooth_color = (0, 255, 0) if smoothing_enabled else (0, 0, 255)
            smooth_text = f"Smoothing: {smooth_status}"
            cv2.putText(frame, smooth_text, (x, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, smooth_color, 1)
        
        # Smoothing method
        if smoothing_method and smoothing_enabled:
            y += 20
            method_text = f"Method: {smoothing_method[:12]}"
            cv2.putText(frame, method_text, (x, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                   
    def draw_fps(self, frame, fps, position=(10, 30)):
        """
        Draw FPS counter
        
        Args:
            frame: OpenCV image
            fps: Frames per second
            position: (x, y) position
        """
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(frame, fps_text, position, 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                   
    def show_gesture_feedback(self, frame, gesture, duration=1.0):
        """
        Show temporary gesture feedback in center of screen
        
        Args:
            frame: OpenCV image
            gesture: Gesture name
            duration: How long to show (seconds)
        """
        height, width = frame.shape[:2]
        
        feedback_text_map = {
            'space': 'SPACE ADDED',
            'clear': 'CANVAS CLEARED',
            'writing': 'WRITING STARTED',
            'stop': 'WRITING STOPPED'
        }
        
        text = feedback_text_map.get(gesture, '')
        if not text:
            return
            
        # Draw large centered text
        font_scale = 1.5
        thickness = 3
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        
        x = (width - text_size[0]) // 2
        y = (height + text_size[1]) // 2
        
        # Draw background
        cv2.rectangle(frame, (x - 20, y - text_size[1] - 20), 
                     (x + text_size[0] + 20, y + 20), (0, 0, 0), -1)
        
        # Draw text
        color = self.colors.get(gesture, (255, 255, 255))
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)