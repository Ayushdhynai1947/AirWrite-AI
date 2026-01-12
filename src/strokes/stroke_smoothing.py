import numpy as np
from scipy.interpolate import splprep, splev
from scipy.signal import savgol_filter

class StrokeSmoother:
    """Advanced stroke smoothing and noise reduction algorithms"""
    
    def __init__(self):
        """Initialize stroke smoother"""
        self.smoothing_methods = {
            'moving_average': self.moving_average_smooth,
            'gaussian': self.gaussian_smooth,
            'savitzky_golay': self.savitzky_golay_smooth,
            'spline': self.spline_smooth,
            'kalman': self.kalman_smooth
        }
        
        # Kalman filter state
        self.kalman_state = None
        self.kalman_covariance = None
        
    def moving_average_smooth(self, points, window_size=5):
        """
        Simple moving average smoothing
        
        Args:
            points: List of (x, y) tuples
            window_size: Size of the moving window
            
        Returns:
            List of smoothed (x, y) points
        """
        if len(points) < window_size:
            return points
            
        points_array = np.array(points)
        smoothed = np.zeros_like(points_array)
        
        for i in range(len(points)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(points), i + window_size // 2 + 1)
            smoothed[i] = np.mean(points_array[start_idx:end_idx], axis=0)
            
        return [tuple(p) for p in smoothed.astype(int)]
        
    def gaussian_smooth(self, points, sigma=2.0):
        """
        Gaussian smoothing using weighted average
        
        Args:
            points: List of (x, y) tuples
            sigma: Standard deviation for Gaussian kernel
            
        Returns:
            List of smoothed (x, y) points
        """
        if len(points) < 3:
            return points
            
        points_array = np.array(points, dtype=float)
        window_size = int(6 * sigma)
        
        if window_size % 2 == 0:
            window_size += 1
            
        # Create Gaussian kernel
        x = np.arange(window_size) - window_size // 2
        kernel = np.exp(-0.5 * (x / sigma) ** 2)
        kernel = kernel / kernel.sum()
        
        # Apply convolution
        smoothed = np.zeros_like(points_array)
        for dim in range(2):
            smoothed[:, dim] = np.convolve(points_array[:, dim], kernel, mode='same')
            
        return [tuple(p) for p in smoothed.astype(int)]
        
    def savitzky_golay_smooth(self, points, window_length=11, polyorder=3):
        """
        Savitzky-Golay filter for smooth differentiation
        
        Args:
            points: List of (x, y) tuples
            window_length: Length of the filter window (must be odd)
            polyorder: Order of the polynomial
            
        Returns:
            List of smoothed (x, y) points
        """
        if len(points) < window_length:
            return points
            
        # Ensure window_length is odd
        if window_length % 2 == 0:
            window_length += 1
            
        # Ensure window_length > polyorder
        window_length = max(window_length, polyorder + 2)
        
        if len(points) < window_length:
            return self.moving_average_smooth(points, window_size=len(points) // 2)
            
        points_array = np.array(points, dtype=float)
        
        try:
            smoothed = np.zeros_like(points_array)
            smoothed[:, 0] = savgol_filter(points_array[:, 0], window_length, polyorder)
            smoothed[:, 1] = savgol_filter(points_array[:, 1], window_length, polyorder)
            return [tuple(p) for p in smoothed.astype(int)]
        except Exception as e:
            # Fallback to moving average if Savitzky-Golay fails
            return self.moving_average_smooth(points)
            
    def spline_smooth(self, points, smoothing_factor=0.0, num_points=None):
        """
        B-spline interpolation for smooth curves
        
        Args:
            points: List of (x, y) tuples
            smoothing_factor: Smoothing parameter (0 = interpolate exactly)
            num_points: Number of points in output (None = same as input)
            
        Returns:
            List of smoothed (x, y) points
        """
        if len(points) < 4:
            return points
            
        points_array = np.array(points, dtype=float)
        
        try:
            # Parametric spline interpolation
            tck, u = splprep([points_array[:, 0], points_array[:, 1]], 
                            s=smoothing_factor, k=min(3, len(points) - 1))
            
            # Generate smooth curve
            if num_points is None:
                num_points = len(points)
                
            u_new = np.linspace(0, 1, num_points)
            x_new, y_new = splev(u_new, tck)
            
            smoothed = np.column_stack([x_new, y_new])
            return [tuple(p) for p in smoothed.astype(int)]
        except Exception as e:
            # Fallback to Gaussian smoothing if spline fails
            return self.gaussian_smooth(points)
            
    def kalman_smooth(self, points, process_variance=1e-5, measurement_variance=1e-1):
        """
        Kalman filter for real-time smoothing
        
        Args:
            points: List of (x, y) tuples
            process_variance: Process noise variance
            measurement_variance: Measurement noise variance
            
        Returns:
            List of smoothed (x, y) points
        """
        if len(points) < 2:
            return points
            
        smoothed = []
        
        # Initialize Kalman filter
        state = np.array([points[0][0], points[0][1], 0, 0], dtype=float)  # [x, y, vx, vy]
        covariance = np.eye(4) * 1000
        
        # State transition matrix (constant velocity model)
        F = np.array([[1, 0, 1, 0],
                     [0, 1, 0, 1],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], dtype=float)
        
        # Measurement matrix
        H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]], dtype=float)
        
        # Process and measurement noise
        Q = np.eye(4) * process_variance
        R = np.eye(2) * measurement_variance
        
        for point in points:
            # Prediction
            state = F @ state
            covariance = F @ covariance @ F.T + Q
            
            # Update
            measurement = np.array(point, dtype=float)
            y = measurement - H @ state
            S = H @ covariance @ H.T + R
            K = covariance @ H.T @ np.linalg.inv(S)
            
            state = state + K @ y
            covariance = (np.eye(4) - K @ H) @ covariance
            
            smoothed.append((int(state[0]), int(state[1])))
            
        return smoothed
        
    def remove_duplicates(self, points, min_distance=2):
        """
        Remove duplicate or very close points
        
        Args:
            points: List of (x, y) tuples
            min_distance: Minimum distance between points
            
        Returns:
            List of filtered points
        """
        if len(points) < 2:
            return points
            
        filtered = [points[0]]
        
        for point in points[1:]:
            last_point = filtered[-1]
            distance = np.sqrt((point[0] - last_point[0])**2 + (point[1] - last_point[1])**2)
            
            if distance >= min_distance:
                filtered.append(point)
                
        return filtered
        
    def douglas_peucker_simplify(self, points, epsilon=2.0):
        """
        Douglas-Peucker algorithm for curve simplification
        
        Args:
            points: List of (x, y) tuples
            epsilon: Simplification tolerance
            
        Returns:
            List of simplified points
        """
        if len(points) < 3:
            return points
            
        def perpendicular_distance(point, line_start, line_end):
            """Calculate perpendicular distance from point to line"""
            if line_start == line_end:
                return np.sqrt((point[0] - line_start[0])**2 + (point[1] - line_start[1])**2)
                
            numerator = abs((line_end[1] - line_start[1]) * point[0] - 
                          (line_end[0] - line_start[0]) * point[1] + 
                          line_end[0] * line_start[1] - 
                          line_end[1] * line_start[0])
            denominator = np.sqrt((line_end[1] - line_start[1])**2 + 
                                (line_end[0] - line_start[0])**2)
            
            return numerator / denominator
            
        def simplify_recursive(pts):
            """Recursive simplification"""
            if len(pts) < 3:
                return pts
                
            # Find point with maximum distance
            max_distance = 0
            max_index = 0
            
            for i in range(1, len(pts) - 1):
                distance = perpendicular_distance(pts[i], pts[0], pts[-1])
                if distance > max_distance:
                    max_distance = distance
                    max_index = i
                    
            # If max distance is greater than epsilon, split
            if max_distance > epsilon:
                left = simplify_recursive(pts[:max_index + 1])
                right = simplify_recursive(pts[max_index:])
                return left[:-1] + right
            else:
                return [pts[0], pts[-1]]
                
        return simplify_recursive(points)
        
    def smooth_stroke(self, points, method='savitzky_golay', **kwargs):
        """
        Apply smoothing to a stroke
        
        Args:
            points: List of (x, y) tuples
            method: Smoothing method name
            **kwargs: Additional arguments for the smoothing method
            
        Returns:
            List of smoothed points
        """
        if len(points) < 2:
            return points
            
        # Remove duplicates first
        points = self.remove_duplicates(points)
        
        if len(points) < 2:
            return points
            
        # Apply selected smoothing method
        if method in self.smoothing_methods:
            smoothed = self.smoothing_methods[method](points, **kwargs)
        else:
            smoothed = points
            
        return smoothed
        
    def multi_pass_smooth(self, points, methods=None):
        """
        Apply multiple smoothing passes
        
        Args:
            points: List of (x, y) tuples
            methods: List of (method_name, kwargs) tuples
            
        Returns:
            List of smoothed points
        """
        if methods is None:
            methods = [
                ('kalman', {'process_variance': 1e-5, 'measurement_variance': 1e-1}),
                ('savitzky_golay', {'window_length': 7, 'polyorder': 3}),
                ('gaussian', {'sigma': 1.5})
            ]
            
        result = points
        
        for method_name, kwargs in methods:
            if len(result) >= 2:
                result = self.smooth_stroke(result, method=method_name, **kwargs)
                
        return result