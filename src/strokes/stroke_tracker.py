import numpy as np
import time

class StrokeTracker:
    """Tracks and manages writing strokes"""
    
    def __init__(self, min_distance_threshold=5):
        """
        Initialize stroke tracker
        
        Args:
            min_distance_threshold: Minimum distance to add a new point (reduces noise)
        """
        self.current_stroke = []
        self.all_strokes = []
        self.is_tracking = False
        self.min_distance_threshold = min_distance_threshold
        self.last_point = None
        self.stroke_start_time = None
        
    def start_stroke(self, point):
        """
        Start a new stroke
        
        Args:
            point: (x, y) starting point
        """
        self.current_stroke = [point]
        self.is_tracking = True
        self.last_point = point
        self.stroke_start_time = time.time()
        
    def add_point(self, point):
        """
        Add a point to current stroke if far enough from last point
        
        Args:
            point: (x, y) point to add
            
        Returns:
            bool: True if point was added, False otherwise
        """
        if not self.is_tracking:
            return False
            
        if self.last_point is None:
            self.current_stroke.append(point)
            self.last_point = point
            return True
            
        # Calculate distance from last point
        distance = np.sqrt(
            (point[0] - self.last_point[0])**2 + 
            (point[1] - self.last_point[1])**2
        )
        
        # Only add if moved enough (reduces jitter)
        if distance >= self.min_distance_threshold:
            self.current_stroke.append(point)
            self.last_point = point
            return True
            
        return False
        
    def end_stroke(self):
        """
        End current stroke and save it
        
        Returns:
            list: The completed stroke points
        """
        if not self.is_tracking:
            return None
            
        self.is_tracking = False
        
        # Only save strokes with enough points
        if len(self.current_stroke) >= 3:
            stroke_data = {
                'points': self.current_stroke.copy(),
                'timestamp': self.stroke_start_time,
                'duration': time.time() - self.stroke_start_time
            }
            self.all_strokes.append(stroke_data)
            completed_stroke = self.current_stroke.copy()
            self.current_stroke = []
            return completed_stroke
            
        self.current_stroke = []
        return None
        
    def get_current_stroke(self):
        """Get current stroke being drawn"""
        return self.current_stroke
        
    def get_all_strokes(self):
        """Get all completed strokes"""
        return self.all_strokes
        
    def clear_all_strokes(self):
        """Clear all strokes"""
        self.current_stroke = []
        self.all_strokes = []
        self.is_tracking = False
        self.last_point = None
        
    def clear_last_stroke(self):
        """Remove the last completed stroke"""
        if self.all_strokes:
            return self.all_strokes.pop()
        return None
        
    def get_stroke_count(self):
        """Get number of completed strokes"""
        return len(self.all_strokes)
        
    def is_drawing(self):
        """Check if currently drawing"""
        return self.is_tracking