import sys
print(sys.path)
import os
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import scoliomorph.analysis as sma

# Example usage
folder_path = "./stl"  # Path to your folder with STL files

# Calculate the vertebral column geometric properties for each STL file
stl_properties = sma.calculate_vbc_profile(folder_path)

# Print out the results
for item in stl_properties:
    print(f"File: {item['filename']}")
    print(f"Pitch: {item['pitch']:.2f}°, Roll: {item['roll']:.2f}°, Yaw: {item['yaw']:.2f}°")
    print(f"Centroid: {item['centroid']}\n")

# Plot the stacked points with vectors showing angles
# sma.plot_vbc_profile(stl_properties)

# Plot the stacked vertebral bodies with STL files. slow with limited memory. careful with large number of files
sma.plot_stl_files(folder_path, plot_type='mesh', color='red', alpha=0.6)