import sys
print(sys.path)
import os
import numpy as np
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scoliomorph.analysis import load_stl_file, calculate_principal_axes, plot_point_cloud_fixed_axes

single_file = False
# Example usage
if single_file:
    # Path to the STL directory
    stl_dir = os.path.join(os.path.dirname(__file__), '..', 'stl')

    # Example STL file
    stl_file_path = os.path.join(stl_dir, '01_CTACardio segmentation_L3 vertebra.stl')

    # Now you can pass `stl_file_path` to your load_stl_file function
    points = load_stl_file(stl_file_path)
    pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(points)
    plot_point_cloud_fixed_axes(centered_points, principal_axes, pitch, roll, yaw)
    
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
            
            # Select points below y=0, only the body part. Test method
            # selected_points = centered_points[centered_points[:, 1] < 0]
            
            # Continue with the original point cloud
            selected_points = points
            
            # Calculate pitch, roll, and yaw
            pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(selected_points)
            
            # Plot the 3D point cloud with fixed axes
            plot_point_cloud_fixed_axes(centered_points, principal_axes, pitch, roll, yaw)