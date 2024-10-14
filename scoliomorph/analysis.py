import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
import os
import trimesh

def load_stl_file(filepath):
    """Load STL file and extract the points from the mesh."""
    your_mesh = mesh.Mesh.from_file(filepath)
    points = your_mesh.vectors.reshape(-1, 3)
    return points

def calculate_principal_axes(selected_points):
    """Calculate pitch, roll, yaw based on the principal axes of the point cloud."""
    centroid = np.mean(selected_points, axis=0)
    centered_points = selected_points - centroid
    cov_matrix = np.cov(centered_points.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    
    # Define axes
    x_axis = sorted_eigenvectors[:, 0]
    y_axis = sorted_eigenvectors[:, 1]
    z_axis = sorted_eigenvectors[:, 2]
    
    # Pitch: rotation around X-axis
    pitch = normalize_angles(np.arctan2(x_axis[2], x_axis[1]) * 180 / np.pi)
    
    # Roll: rotation around Y-axis
    roll = normalize_angles(np.arctan2(y_axis[2], y_axis[0]) * 180 / np.pi)
    
    # Yaw: rotation around Z-axis
    yaw = normalize_angles(np.arctan2(z_axis[1], z_axis[0]) * 180 / np.pi)
    
    return pitch, roll, yaw, centroid, centered_points, sorted_eigenvectors

# Function to calculate and store results
def calculate_vbc_profile(folder_path):
    result = []

    # Loop through sorted STL files in the folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".stl"):
            filepath = os.path.join(folder_path, filename)
            points = load_stl_file(filepath)
            
            # Calculate pitch, roll, and yaw
            pitch, roll, yaw, centroid, centered_points, principal_axes = calculate_principal_axes(points)
            
            # Store the results in a structure
            result.append({
                "filename": filename,
                "pitch": pitch,
                "roll": roll,
                "yaw": yaw,
                "centroid": centroid,
                "principal_axes": principal_axes
            })
    
    return result

def plot_2d_angles_with_labels(pitch, roll, yaw, principal_axes, centered_points):
    """Plot the pitch, roll, yaw along with the point cloud projections."""
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    scale = 50

    # Plot Pitch (YZ-plane projection)
    axs[0].scatter(centered_points[:, 1], centered_points[:, 2], s=1, color='gray', alpha=0.5)  # Projection on YZ-plane
    axs[0].plot([-scale, scale], [0, 0], color='r', linewidth=1, label='Global Z Axis')
    # Plot the Pitch Axis in both positive and negative directions in one line
    axs[0].plot([0, principal_axes[1, 0] * scale, -principal_axes[1, 0] * scale],
            [0, principal_axes[2, 0] * scale, -principal_axes[2, 0] * scale],
            color='r', linestyle='--', linewidth=0.75, label='Pitch Axis')
    axs[0].set_xlim(-scale, scale)
    axs[0].set_ylim(-scale, scale)
    axs[0].set_title(f'Pitch: {pitch:.2f}° (YZ-plane)')
    axs[0].set_xlabel('Z-axis')
    axs[0].set_ylabel('Y-axis')
    axs[0].legend()

    # Add angle label for pitch
    # axs[0].text(principal_axes[1, 0] * scale / 2, principal_axes[2, 0] * scale / 2, f'{pitch:.2f}°', color='r')

    # Plot Roll (XZ-plane projection)
    axs[1].scatter(centered_points[:, 0], centered_points[:, 2], s=1, color='gray', alpha=0.5)  # Projection on XZ-plane
    axs[1].plot([-scale, scale], [0, 0], color='g', linewidth=1, label='Global X Axis')
    # Plot the Roll Axis in both positive and negative directions in one line
    axs[1].plot([0, principal_axes[0, 1] * scale, -principal_axes[0, 1] * scale], 
            [0, principal_axes[2, 1] * scale, -principal_axes[2, 1] * scale],
            color='g', linestyle='--', linewidth=0.75, label='Roll Axis')
    axs[1].set_xlim(-scale, scale)
    axs[1].set_ylim(-scale, scale)
    axs[1].set_title(f'Roll: {roll:.2f}° (XZ-plane)')
    axs[1].set_xlabel('X-axis')
    axs[1].set_ylabel('Z-axis')
    axs[1].legend()

    # Add angle label for roll
    # axs[1].text(principal_axes[0, 1] * scale / 2, principal_axes[2, 1] * scale / 2, f'{roll:.2f}°', color='g')

    # Plot Yaw (XY-plane projection)
    axs[2].scatter(centered_points[:, 0], centered_points[:, 1], s=1, color='gray', alpha=0.5)  # Projection on XY-plane
    axs[2].plot([-scale, scale], [0, 0], color='b', linewidth=1, label='Global X Axis')
    # Plot the Yaw Axis in both positive and negative directions in one line
    axs[2].plot([0, principal_axes[0, 2] * scale, -principal_axes[0, 2] * scale], 
            [0, principal_axes[1, 2] * scale, -principal_axes[1, 2] * scale],
            color='b', linestyle='--', linewidth=0.75, label='Yaw Axis')
    axs[2].set_xlim(-scale, scale)
    axs[2].set_ylim(-scale, scale)
    axs[2].set_title(f'Yaw: {yaw:.2f}° (XY-plane)')
    axs[2].set_xlabel('X-axis')
    axs[2].set_ylabel('Y-axis')
    axs[2].legend()

    # Add angle label for yaw
    # axs[2].text(principal_axes[0, 2] * scale / 2, principal_axes[1, 2] * scale / 2, f'{yaw:.2f}°', color='b')

    # Show the 2D plot
    plt.tight_layout()
    plt.show()
    

# Function to plot point cloud and principal axes with fixed global coordinate system and angular lines
def plot_point_cloud_fixed_axes(centered_points, principal_axes, pitch, roll, yaw):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Adjust points by centroid shift to simulate stacking
    # adjusted_points = centered_points + prev_centroid_shift
    # If you want to disable stacking correction, comment the line above and uncomment the line below
    adjusted_points = centered_points
    
    # Plot points
    ax.scatter(adjusted_points[:, 0], adjusted_points[:, 1], adjusted_points[:, 2], s=1, color='gray', alpha=0.5)
    
    # Define the scale of the axes
    scale = 50
    
    # Plot global X, Y, Z axes for reference (fixed global coordinate system)
    ax.quiver(0, 0, 0, scale, 0, 0, color='r', label='Global X Axis')
    ax.quiver(0, 0, 0, 0, scale, 0, color='g', label='Global Y Axis')
    ax.quiver(0, 0, 0, 0, 0, scale, color='b', label='Global Z Axis')

    # Plot lines to show angular rotation relative to the global axes
    # Red line for X-axis
    ax.plot([0, principal_axes[0, 0] * scale], [0, principal_axes[1, 0] * scale], [0, principal_axes[2, 0] * scale], 
            color='r', linestyle='--', linewidth=0.8, label='Pitch Angle')

    # Green line for Y-axis
    ax.plot([0, principal_axes[0, 1] * scale], [0, principal_axes[1, 1] * scale], [0, principal_axes[2, 1] * scale], 
            color='g', linestyle='--', linewidth=0.8, label='Roll Angle')

    # Blue line for Z-axis
    ax.plot([0, principal_axes[0, 2] * scale], [0, principal_axes[1, 2] * scale], [0, principal_axes[2, 2] * scale], 
            color='b', linestyle='--', linewidth=0.8, label='Yaw Angle')

    # Show the angles in a consistent reference frame
    ax.text2D(0.05, 0.95, f'Pitch: {pitch:.2f}°\nRoll: {roll:.2f}°\nYaw: {yaw:.2f}°', transform=ax.transAxes)
    
    # Set labels and fixed view
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=20, azim=30)  # Fix view for consistency across plots
    
    # Show plot
    plt.show()
    

def plot_stl_files(folder_path, plot_type='pointcloud', color='blue', alpha=1.0):
    """
    Function to load STL files from a folder, align points to (x, y) = (0, 0), and plot them.
    
    Parameters:
    folder_path : str
        Path to the folder containing STL files.
    plot_type : str
        Type of plot ('pointcloud' or 'mesh'). Default is 'pointcloud'.
    color : str
        Color for the plot (e.g., 'red', 'blue'). Default is 'blue'.
    alpha : float
        Transparency level for the plot (0.0 to 1.0). Default is 1.0 (opaque).
    """
    
    # Set up the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Iterate through all STL files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".stl"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            
            # Load the STL file
            mesh = trimesh.load(file_path)

            # Get the vertices (points)
            vertices = mesh.vertices

            # Calculate centroid and shift points so that the centroid is at (x=0, y=0)
            centroid = np.mean(vertices, axis=0)
            aligned_vertices = vertices - [centroid[0], centroid[1], 0]  # Only adjust x, y
            
            # Plot based on the chosen plot type
            if plot_type == 'pointcloud':
                ax.scatter(aligned_vertices[:, 0], aligned_vertices[:, 1], aligned_vertices[:, 2], 
                           color=color, alpha=alpha, label=filename)
            elif plot_type == 'mesh':
                faces = mesh.faces
                ax.plot_trisurf(aligned_vertices[:, 0], aligned_vertices[:, 1], aligned_vertices[:, 2], 
                                triangles=faces, color=color, alpha=alpha, label=filename)
    
    # Add labels and legend
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    plt.title('Aligned STL Files')
    # plt.legend() # Uncomment to show legend
    # Set equal aspect ratio for 3D plot
    set_axes_equal(ax)
    plt.show()

    
# Function to plot stacked points with vectors showing angles
def plot_vbc_profile(result):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # To stack the point clouds, we'll need to adjust centroids to align them
    cumulative_shift = np.zeros(3)
    scale = 30  # Length of the vector for visualizing the axes

    # Loop through the result structure to plot each point cloud
    for item in result:
        centroid = item['centroid'] 
        
        # Plot the centroid as a point
        ax.scatter(centroid[0], centroid[1], centroid[2], color='black', s=20)
        
       # Plot the principal axes (showing pitch, roll, yaw) as vectors

        # Plot Pitch Axis (Positive and Negative directions)
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                item['principal_axes'][0, 0] * scale, 
                item['principal_axes'][1, 0] * scale, 
                item['principal_axes'][2, 0] * scale, 
                color='r', label='Pitch Axis (Positive)')
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                -item['principal_axes'][0, 0] * scale, 
                -item['principal_axes'][1, 0] * scale, 
                -item['principal_axes'][2, 0] * scale, 
                color='r', linestyle='--', label='Pitch Axis (Negative)')

        # Plot Roll Axis (Positive and Negative directions)
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                item['principal_axes'][0, 1] * scale, 
                item['principal_axes'][1, 1] * scale, 
                item['principal_axes'][2, 1] * scale, 
                color='g', label='Roll Axis (Positive)')
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                -item['principal_axes'][0, 1] * scale, 
                -item['principal_axes'][1, 1] * scale, 
                -item['principal_axes'][2, 1] * scale, 
                color='g', linestyle='--', label='Roll Axis (Negative)')

        # Plot Yaw Axis (Positive and Negative directions)
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                item['principal_axes'][0, 2] * scale, 
                item['principal_axes'][1, 2] * scale, 
                item['principal_axes'][2, 2] * scale, 
                color='b', label='Yaw Axis (Positive)')
        ax.quiver(centroid[0], centroid[1], centroid[2], 
                -item['principal_axes'][0, 2] * scale, 
                -item['principal_axes'][1, 2] * scale, 
                -item['principal_axes'][2, 2] * scale, 
                color='b', linestyle='--', label='Yaw Axis (Negative)')

        # Update cumulative shift to stack the next cloud on top
        cumulative_shift += item['centroid']

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.title('Stacked Point Clouds with Pitch, Roll, Yaw Vectors')

    # Set equal aspect ratio for 3D plot
    set_axes_equal(ax)

    plt.show()


def normalize_angles(angle):
    """
    Normalize pitch, roll, and yaw to stay within the range [-90°, +90°]
    by converting them to their complementary angles if they exceed 90° or -90°.
    """
    def normalize_angle(angle):
        """Normalize an individual angle to stay within [-90°, 90°]."""
        if angle > 90:
            return angle - 180
        elif angle < -90:
            return angle + 180
        return angle

    # Normalize pitch, roll, and yaw
    normalized_angle = normalize_angle(angle)
    return normalized_angle

def set_axes_equal(ax):
    """Set 3D plot axes to equal scale."""
    limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
    spans = np.abs(limits[:, 1] - limits[:, 0])
    centers = np.mean(limits, axis=1)
    max_span = max(spans)
    
    # Set the axis limits to be centered and proportional
    ax.set_xlim3d([centers[0] - max_span / 2, centers[0] + max_span / 2])
    ax.set_ylim3d([centers[1] - max_span / 2, centers[1] + max_span / 2])
    ax.set_zlim3d([centers[2] - max_span / 2, centers[2] + max_span / 2])
