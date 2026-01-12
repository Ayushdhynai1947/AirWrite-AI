
import numpy as np
import time
from src.strokes.stroke_smoothing import StrokeSmoother

class StrokeTracker:
    """Tracks and manages writing strokes with smoothing"""
    
    def __init__(self, min_distance_threshold=5, enable_smoothing=True, smoothing_method='savitzky_golay'):
        """
        Initialize stroke tracker
        
        Args:
            min_distance_threshold: Minimum distance to add a new point (reduces noise)
            enable_smoothing: Enable automatic stroke smoothing
            smoothing_method: Smoothing method to use
        """
        self.current_stroke = []
        self.current_stroke_raw = []  # Store raw points before smoothing
        self.all_strokes = []
        self.is_tracking = False
        self.min_distance_threshold = min_distance_threshold
        self.last_point = None
        self.stroke_start_time = None
        
        # Smoothing
        self.enable_smoothing = enable_smoothing
        self.smoothing_method = smoothing_method
        self.smoother = StrokeSmoother()
        self.real_time_smooth = True  # Apply smoothing in real-time
        
    def start_stroke(self, point):
        """
        Start a new stroke
        
        Args:
            point: (x, y) starting point
        """
        self.current_stroke = [point]
        self.current_stroke_raw = [point]
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
            self.current_stroke_raw.append(point)
            self.last_point = point
            self._update_smoothed_stroke()
            return True
            
        # Calculate distance from last point
        distance = np.sqrt(
            (point[0] - self.last_point[0])**2 + 
            (point[1] - self.last_point[1])**2
        )
        
        # Only add if moved enough (reduces jitter)
        if distance >= self.min_distance_threshold:
            self.current_stroke_raw.append(point)
            self.last_point = point
            self._update_smoothed_stroke()
            return True
            
        return False
        
    def _update_smoothed_stroke(self):
        """Update the smoothed version of current stroke"""
        if self.enable_smoothing and self.real_time_smooth and len(self.current_stroke_raw) > 3:
            # Apply real-time smoothing
            self.current_stroke = self.smoother.smooth_stroke(
                self.current_stroke_raw,
                method=self.smoothing_method,
                window_length=min(7, len(self.current_stroke_raw)),
                polyorder=min(3, len(self.current_stroke_raw) - 1)
            )
        else:
            self.current_stroke = self.current_stroke_raw.copy()
        
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
        if len(self.current_stroke_raw) >= 3:
            # Apply final smoothing pass
            if self.enable_smoothing:
                smoothed_points = self.smoother.multi_pass_smooth(self.current_stroke_raw)
            else:
                smoothed_points = self.current_stroke_raw.copy()
            
            stroke_data = {
                'points': smoothed_points,
                'raw_points': self.current_stroke_raw.copy(),
                'timestamp': self.stroke_start_time,
                'duration': time.time() - self.stroke_start_time,
                'point_count': len(self.current_stroke_raw),
                'smoothed_count': len(smoothed_points)
            }
            self.all_strokes.append(stroke_data)
            completed_stroke = smoothed_points.copy()
            self.current_stroke = []
            self.current_stroke_raw = []
            return completed_stroke
            
        self.current_stroke = []
        self.current_stroke_raw = []
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
        self.current_stroke_raw = []
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
        
    def get_raw_stroke(self):
        """Get current raw (unsmoothed) stroke"""
        return self.current_stroke_raw
        
    def toggle_smoothing(self):
        """Toggle smoothing on/off"""
        self.enable_smoothing = not self.enable_smoothing
        return self.enable_smoothing
        
    def set_smoothing_method(self, method):
        """
        Set the smoothing method
        
        Args:
            method: One of 'moving_average', 'gaussian', 'savitzky_golay', 'spline', 'kalman'
        """
        if method in self.smoother.smoothing_methods:
            self.smoothing_method = method
            return True
        return False
        
    def export_stroke_data(self, stroke_index=None):
        """
        Export stroke data for analysis or storage
        
        Args:
            stroke_index: Index of stroke to export (None = all strokes)
            
        Returns:
            dict or list: Stroke data
        """
        if stroke_index is not None:
            if 0 <= stroke_index < len(self.all_strokes):
                return self.all_strokes[stroke_index]
            return None
        return self.all_strokes