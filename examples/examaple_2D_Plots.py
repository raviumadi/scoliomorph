import sys
print(sys.path)

from vbr_lib.vbr.analysis import load_stl_file, calculate_principal_axes, plot_2d_angles_with_labels
import os

# Example usage
points = load_stl_file("../stl/")
pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(points)
plot_2d_angles_with_labels(pitch, roll, yaw, principal_axes, centered_points)
