import numpy as np
import matplotlib.pyplot as plt
from stl import mesh

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
    pitch = np.arctan2(x_axis[2], x_axis[1]) * 180 / np.pi
    
    # Roll: rotation around Y-axis
    roll = np.arctan2(y_axis[2], y_axis[0]) * 180 / np.pi
    
    # Yaw: rotation around Z-axis
    yaw = np.arctan2(z_axis[1], z_axis[0]) * 180 / np.pi
    
    return pitch, roll, yaw, centroid, centered_points, sorted_eigenvectors

def plot_2d_angles_with_labels(pitch, roll, yaw, principal_axes, centered_points):
    """Plot the pitch, roll, yaw along with the point cloud projections."""
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    scale = 50

    # Plot Pitch (YZ-plane projection)
    axs[0].scatter(centered_points[:, 1], centered_points[:, 2], s=1, color='gray', alpha=0.5)  # Projection on YZ-plane
    axs[0].plot([0, scale], [0, 0], color='r', linewidth=2, label='Global Z Axis')
    axs[0].plot([0, principal_axes[1, 0] * scale], [0, principal_axes[2, 0] * scale], color='r', linestyle='--', label='Pitch Axis')
    axs[0].set_xlim(-scale, scale)
    axs[0].set_ylim(-scale, scale)
    axs[0].set_title(f'Pitch: {pitch:.2f}° (YZ-plane)')
    axs[0].set_xlabel('Z-axis')
    axs[0].set_ylabel('Y-axis')
    axs[0].legend()

    # Add angle label for pitch
    axs[0].text(principal_axes[1, 0] * scale / 2, principal_axes[2, 0] * scale / 2, f'{pitch:.2f}°', color='r')

    # Plot Roll (XZ-plane projection)
    axs[1].scatter(centered_points[:, 0], centered_points[:, 2], s=1, color='gray', alpha=0.5)  # Projection on XZ-plane
    axs[1].plot([0, scale], [0, 0], color='g', linewidth=2, label='Global X Axis')
    axs[1].plot([0, principal_axes[0, 1] * scale], [0, principal_axes[2, 1] * scale], color='g', linestyle='--', label='Roll Axis')
    axs[1].set_xlim(-scale, scale)
    axs[1].set_ylim(-scale, scale)
    axs[1].set_title(f'Roll: {roll:.2f}° (XZ-plane)')
    axs[1].set_xlabel('X-axis')
    axs[1].set_ylabel('Z-axis')
    axs[1].legend()

    # Add angle label for roll
    axs[1].text(principal_axes[0, 1] * scale / 2, principal_axes[2, 1] * scale / 2, f'{roll:.2f}°', color='g')

    # Plot Yaw (XY-plane projection)
    axs[2].scatter(centered_points[:, 0], centered_points[:, 1], s=1, color='gray', alpha=0.5)  # Projection on XY-plane
    axs[2].plot([0, scale], [0, 0], color='b', linewidth=2, label='Global X Axis')
    axs[2].plot([0, principal_axes[0, 2] * scale], [0, principal_axes[1, 2] * scale], color='b', linestyle='--', label='Yaw Axis')
    axs[2].set_xlim(-scale, scale)
    axs[2].set_ylim(-scale, scale)
    axs[2].set_title(f'Yaw: {yaw:.2f}° (XY-plane)')
    axs[2].set_xlabel('X-axis')
    axs[2].set_ylabel('Y-axis')
    axs[2].legend()

    # Add angle label for yaw
    axs[2].text(principal_axes[0, 2] * scale / 2, principal_axes[1, 2] * scale / 2, f'{yaw:.2f}°', color='b')

    # Show the 2D plot
    plt.tight_layout()
    plt.show()