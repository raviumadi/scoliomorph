import sys
print(sys.path)
import os
import numpy as np
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scoliomorph.analysis import load_stl_file, calculate_principal_axes, plot_2d_angles_with_labels

single_file = True

if single_file:
    # Example usage - single file

    # Path to the STL directory
    stl_dir = os.path.join(os.path.dirname(__file__), '..', 'stl')

    # Example STL file
    stl_file_path = os.path.join(stl_dir, '04_CTACardio segmentation_T12 vertebra.stl')

    # Now you can pass `stl_file_path` to your load_stl_file function
    points = load_stl_file(stl_file_path)
    pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(points)
    plot_2d_angles_with_labels(pitch, roll, yaw, principal_axes, centered_points)

else:
    # Example usage - all files
    # Directory with STL files
    folder_path = "./stl"

    # Loop through sorted STL files in the folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".stl"):
            filepath = os.path.join(folder_path, filename)
            points = load_stl_file(filepath)
            
            # Center the point cloud
            centroid = np.mean(points, axis=0)
            centered_points = points - centroid
            
            # Select points below y=0
            # selected_points = centered_points[centered_points[:, 1] < 0]
            # Check with the original point cloud
            selected_points = points
            
            # Calculate pitch, roll, and yaw
            pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(selected_points)
            
            # Plot the 2D angles along with the point cloud projections and angle labels
            plot_2d_angles_with_labels(pitch, roll, yaw, principal_axes, centered_points)