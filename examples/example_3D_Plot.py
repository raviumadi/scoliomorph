import sys
print(sys.path)
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scoliomorph.analysis import load_stl_file, calculate_principal_axes, plot_point_cloud_fixed_axes


# Example usage
# Path to the STL directory
stl_dir = os.path.join(os.path.dirname(__file__), '..', 'stl')

# Example STL file
stl_file_path = os.path.join(stl_dir, '01_CTACardio segmentation_L3 vertebra.stl')

# Now you can pass `stl_file_path` to your load_stl_file function
points = load_stl_file(stl_file_path)
pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(points)
plot_point_cloud_fixed_axes(centered_points, principal_axes, pitch, roll, yaw)