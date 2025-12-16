---
sidebar_label: 'Sensor Fusion and Perception'
sidebar_position: 10
slug: /docs/9-sensor-fusion-and-perception
---

# Sensor Fusion and Perception

## Introduction to Robot Perception

Robot perception involves processing sensory information to understand and interact with the environment. This chapter covers sensor fusion techniques that combine data from multiple sensors to create a coherent understanding of the world.

## Types of Robot Sensors

### Vision Sensors
- **RGB Cameras**: Provide color images for object recognition
- **Stereo Cameras**: Enable depth estimation through disparity
- **RGB-D Cameras**: Provide color and depth information
- **Event Cameras**: Ultra-fast response to changes in brightness

### Range Sensors
- **LiDAR**: Light Detection and Ranging for precise 3D mapping
- **RADAR**: Radio Detection and Ranging, works in all weather
- **Ultrasonic Sensors**: Short-range distance measurement
- **Time-of-Flight Sensors**: Direct distance measurement

### Inertial Sensors
- **Accelerometers**: Measure linear acceleration
- **Gyroscopes**: Measure angular velocity
- **Magnetometers**: Measure magnetic field
- **Inertial Measurement Units (IMUs)**: Combined inertial sensors

### Tactile and Force Sensors
- **Force/Torque Sensors**: Measure interaction forces
- **Tactile Sensors**: Detect contact and pressure
- **Proximity Sensors**: Detect nearby objects

## Sensor Fusion Fundamentals

### Why Sensor Fusion?

Sensor fusion combines data from multiple sensors to:

- Improve accuracy and precision
- Increase robustness against sensor failures
- Provide information not available from single sensors
- Reduce uncertainty in measurements

### Fusion Architectures

#### Centralized Fusion
All sensor data is processed in a single central node.

#### Distributed Fusion
Each sensor processes data locally, then combines results.

#### Decentralized Fusion
No central node; sensors communicate directly.

## Mathematical Foundations

### Probabilistic Framework

Sensor fusion is typically formulated in a probabilistic framework:

- **State Estimation**: Estimate robot state from sensor measurements
- **Bayesian Inference**: Update beliefs based on new measurements
- **Probability Distributions**: Represent uncertainty in measurements

```python
import numpy as np
from scipy.stats import norm

class ProbabilisticSensorFusion:
    def __init__(self, initial_state, initial_covariance):
        self.state = initial_state  # Mean of state estimate
        self.covariance = initial_covariance  # Covariance matrix
        
    def predict(self, control_input, process_noise):
        """Prediction step in state estimation"""
        # Model-specific prediction (e.g., for position and velocity)
        # x_k = A*x_{k-1} + B*u_k
        A = np.array([[1, 1], [0, 1]])  # Simple motion model
        B = np.array([[0.5], [1.0]])    # Control input matrix
        
        self.state = A @ self.state + B @ control_input
        self.covariance = A @ self.covariance @ A.T + process_noise
        
    def update(self, measurement, sensor_noise, sensor_matrix):
        """Update step with new measurement"""
        # Compute Kalman gain
        innovation_covariance = sensor_matrix @ self.covariance @ sensor_matrix.T + sensor_noise
        kalman_gain = self.covariance @ sensor_matrix.T @ np.linalg.inv(innovation_covariance)
        
        # Update state and covariance
        innovation = measurement - sensor_matrix @ self.state
        self.state = self.state + kalman_gain @ innovation
        self.covariance = (np.eye(len(self.state)) - kalman_gain @ sensor_matrix) @ self.covariance
```

## Kalman Filter Approaches

### Linear Kalman Filter
For linear systems with Gaussian noise.

### Extended Kalman Filter (EKF)
Linearizes nonlinear systems around current estimate.

### Unscented Kalman Filter (UKF)
Uses deterministic sampling to capture nonlinear transformations.

### Particle Filters
Monte Carlo approach suitable for non-Gaussian and multimodal distributions.

```python
class ParticleFilter:
    def __init__(self, num_particles, state_dim):
        self.num_particles = num_particles
        self.state_dim = state_dim
        self.particles = np.random.randn(num_particles, state_dim)
        self.weights = np.ones(num_particles) / num_particles

    def predict(self, control_input, noise_std):
        """Predict particles forward in time"""
        for i in range(self.num_particles):
            # Apply motion model with noise
            self.particles[i] += control_input + np.random.normal(0, noise_std, self.state_dim)

    def update(self, measurement, measurement_function, measurement_noise):
        """Update particle weights based on measurement"""
        for i in range(self.num_particles):
            predicted_measurement = measurement_function(self.particles[i])
            # Calculate likelihood of measurement given particle
            likelihood = norm.pdf(measurement, predicted_measurement, measurement_noise)
            self.weights[i] *= likelihood
        
        # Normalize weights
        self.weights /= np.sum(self.weights)

    def resample(self):
        """Resample particles based on weights"""
        indices = np.random.choice(self.num_particles, 
                                 size=self.num_particles, 
                                 p=self.weights)
        self.particles = self.particles[indices]
        self.weights.fill(1.0 / self.num_particles)

    def estimate(self):
        """Calculate state estimate from particles"""
        return np.average(self.particles, weights=self.weights, axis=0)
```

## Multi-Sensor Integration

### Camera-LiDAR Fusion
Combining visual and 3D information for robust perception.

### Visual-Inertial Odometry (VIO)
Combining camera and IMU data for localization.

### GPS-IMU Integration
Combining global and local positioning systems.

### Force-Visual Fusion
Combining tactile and visual feedback for manipulation.

## Computer Vision for Robotics

### Feature Detection and Matching
- **SIFT/ORB**: Scale-invariant feature detection
- **Deep Features**: CNN-based feature extraction

### Object Detection and Recognition
- **YOLO**: Real-time object detection
- **R-CNN**: Region-based detection
- **Transformer-based Detectors**: Modern attention-based approaches

### Simultaneous Localization and Mapping (SLAM)

SLAM algorithms simultaneously build maps and localize the robot:

#### Visual SLAM
Using visual features for mapping and localization.

#### LiDAR SLAM
Using range data for accurate 3D mapping.

#### Visual-Inertial SLAM
Combining visual and inertial measurements.

```python
class VisualSLAM:
    def __init__(self):
        self.map_points = []
        self.camera_poses = []
        self.current_pose = np.eye(4)  # 4x4 transformation matrix
        
    def process_frame(self, image, features, descriptors):
        """Process a new image frame"""
        if len(self.map_points) == 0:
            # Initialize map
            self.initialize_map(image, features, descriptors)
        else:
            # Track features and update pose
            self.track_frame(image, features, descriptors)
            
    def initialize_map(self, image, features, descriptors):
        """Initialize map from first frame"""
        # Create initial features as map points
        for feature in features:
            self.map_points.append({
                'position': None,  # Will be triangulated later
                'descriptor': descriptors[feature['id']],
                'observations': [feature]
            })
        
    def track_frame(self, image, features, descriptors):
        """Track features and update camera pose"""
        # Match current features with map features
        matches = self.match_features(descriptors)
        
        # Estimate camera pose from matches
        if len(matches) > 5:  # Minimum for pose estimation
            pose_update = self.estimate_pose(matches)
            self.current_pose = self.current_pose @ pose_update
            self.camera_poses.append(self.current_pose.copy())
```

## 3D Perception and Reconstruction

### Point Cloud Processing
- **Registration**: Aligning multiple point clouds
- **Segmentation**: Identifying objects in point clouds
- **Feature Extraction**: Finding 3D features

### Surface Reconstruction
Creating surfaces from point cloud data.

### Mesh Generation
Converting point clouds to polygonal meshes.

## Environmental Understanding

### Semantic Segmentation
Understanding object classes in the environment.

### Scene Understanding
Interpreting the meaning and relationships in scenes.

### Dynamic Object Detection
Identifying and tracking moving objects.

## Uncertainty and Robustness

### Uncertainty Quantification
Understanding and representing uncertainty in perception.

### Outlier Rejection
Handling incorrect measurements and false positives.

### Failure Detection
Detecting when perception systems are failing.

## Real-Time Considerations

### Computational Efficiency
Optimizing perception algorithms for real-time performance.

### Multi-Threading
Parallel processing of multiple sensors and algorithms.

### Edge Computing
Deploying perception on robot hardware.

## Code Snippets

```python
# Example: Multi-sensor fusion using Kalman Filter
class MultiSensorFusion:
    def __init__(self):
        # State: [x, y, vx, vy]
        self.state = np.zeros(4)
        self.covariance = np.eye(4) * 100.0  # Initial uncertainty
        
        # Process noise
        self.process_noise = np.diag([0.1, 0.1, 0.5, 0.5])
        
        # Sensor noise for different modalities
        self.camera_noise = np.diag([0.05, 0.05])  # x, y position
        self.lidar_noise = np.diag([0.02, 0.02])   # x, y position
        self.radar_noise = np.diag([0.1, 0.1, 0.2, 0.2])  # x, y, vx, vy
        
    def predict(self, dt):
        """Prediction step"""
        # State transition model: x_k = A*x_{k-1} + w_k
        A = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.state = A @ self.state
        self.covariance = A @ self.covariance @ A.T + self.process_noise
        
    def update_camera(self, measurement):
        """Update with camera measurement [x, y]"""
        # Measurement matrix H for position only
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # Kalman gain
        S = H @ self.covariance @ H.T + self.camera_noise
        K = self.covariance @ H.T @ np.linalg.inv(S)
        
        # Update state and covariance
        innovation = measurement - H @ self.state
        self.state = self.state + K @ innovation
        self.covariance = (np.eye(4) - K @ H) @ self.covariance
        
    def update_lidar(self, measurement):
        """Update with LiDAR measurement [x, y]"""
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        S = H @ self.covariance @ H.T + self.lidar_noise
        K = self.covariance @ H.T @ np.linalg.inv(S)
        
        innovation = measurement - H @ self.state
        self.state = self.state + K @ innovation
        self.covariance = (np.eye(4) - K @ H) @ self.covariance

# Example: Sensor calibration
def calibrate_camera_intrinsics(image_points, world_points, image_size):
    """Calibrate camera intrinsic parameters"""
    import cv2
    
    # Camera matrix (3x3)
    camera_matrix = np.zeros((3, 3))
    dist_coeffs = np.zeros(4)  # Distortion coefficients
    
    # Calibrate camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        [world_points], [image_points], image_size, camera_matrix, dist_coeffs)
    
    return camera_matrix, dist_coeffs

# Example: LiDAR-camera calibration
def calibrate_lidar_camera(lidar_points, camera_points, camera_matrix, dist_coeffs):
    """Find transformation between LiDAR and camera"""
    import cv2
    
    # Solve for transformation matrix
    _, rvec, tvec = cv2.solvePnP(
        lidar_points, camera_points, camera_matrix, dist_coeffs)
    
    # Convert rotation vector to rotation matrix
    R, _ = cv2.Rodrigues(rvec)
    
    # Create 4x4 transformation matrix
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = tvec.flatten()
    
    return T
```

### Exercises

1.  Implement a sensor fusion system combining camera and IMU data
2.  Create a visual SLAM system using feature-based matching
3.  Design a particle filter for multi-sensor data fusion