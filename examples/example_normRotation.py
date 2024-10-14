import sys
print(sys.path)
import os
import numpy as np
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scoliomorph.analysis import normalize_angles

# Example usage:
pitch = 120   # Input pitch angle in degrees
roll = -150   # Input roll angle in degrees
yaw = 180     # Input yaw angle in degrees

# Normalize the angles
pitch_normalized = normalize_angles(pitch)
roll_normalized = normalize_angles(roll) 
yaw_normalized = normalize_angles(yaw)

print(f"Normalized Pitch: {pitch_normalized:.2f}°")
print(f"Normalized Roll: {roll_normalized:.2f}°")
print(f"Normalized Yaw: {yaw_normalized:.2f}°")