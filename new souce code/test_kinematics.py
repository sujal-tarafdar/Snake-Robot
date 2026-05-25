import os
import numpy as np
import matplotlib.pyplot as plt
from kinematics import OrthogonalSnakeKinematics, calculate_alternate_link_kinematics
from gait_generator import SnakeGaitGenerator

def test_gait_and_kinematics():
    print("=== Testing Snake Robot Gait and Kinematics ===")
    
    num_joints = 12
    link_length = 0.05  # 50 mm
    
    gait_gen = SnakeGaitGenerator(num_joints=num_joints)
    kinematics = OrthogonalSnakeKinematics(num_joints=num_joints, link_length=link_length)
    
    # 1. Compare joint amplitudes (Standard vs. Sigmoid)
    A = 0.8  # Target amplitude (approx 45 degrees in rad)
    omega = 1.0
    lag = 0.5712
    a = 1.0  # Slope
    b = 3.0  # Restricted head joints
    t = 0.0  # Snapshot time
    
    std_angles = gait_gen.generate_serpenoid_gait(t, A, omega, lag)
    sig_angles = gait_gen.generate_sigmoid_gait(t, A, omega, lag, a=a, b=b)
    
    # Let's plot the amplitude envelope for all 12 joints
    joints = np.arange(1, num_joints + 1)
    std_envelope = np.ones(num_joints) * A
    sig_envelope = np.zeros(num_joints)
    for i in range(num_joints):
        n = i + 1  # joint index
        sig_envelope[i] = A / (1.0 + np.exp(-a * (n - b)))
        
    plt.figure(figsize=(10, 5))
    plt.plot(joints, np.degrees(std_envelope), 'o--', label='Standard Serpenoid Envelope', color='#ff7f0e', linewidth=2)
    plt.plot(joints, np.degrees(sig_envelope), 'o-', label='Sigmoid-Stabilized Envelope', color='#1f77b4', linewidth=2)
    plt.axvline(x=b, color='red', linestyle=':', label='Restricted Head Zone Bound (b=3)')
    plt.title('Joint Amplitude Envelope Comparison (Head to Tail)', fontsize=14, fontweight='bold')
    plt.xlabel('Joint Index (n)', fontsize=12)
    plt.ylabel('Max Amplitude (Degrees)', fontsize=12)
    plt.xticks(joints)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    envelope_path = 'gait_amplitude_envelope.png'
    plt.savefig(envelope_path, dpi=300)
    print(f"Saved amplitude envelope plot to: {os.path.abspath(envelope_path)}")
    plt.close()
    
    # 2. Simulate 3D joint positions using Denavit-Hartenberg (D-H) kinematics
    # Let's choose a time step t = 2.0 to see a wave shape
    t_wave = 2.0
    std_angles_wave = gait_gen.generate_serpenoid_gait(t_wave, A, omega, lag)
    sig_angles_wave = gait_gen.generate_sigmoid_gait(t_wave, A, omega, lag, a=a, b=b)
    
    std_positions = kinematics.forward_kinematics(std_angles_wave)
    sig_positions = kinematics.forward_kinematics(sig_angles_wave)
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot Standard Snake
    ax.plot(std_positions[:, 0], std_positions[:, 1], std_positions[:, 2], 
            'o-', color='#e377c2', label='Standard Serpenoid Snake', linewidth=3, markersize=6)
    # Highlight Head
    ax.scatter(std_positions[-1, 0], std_positions[-1, 1], std_positions[-1, 2], 
               color='#d62728', s=100, label='Standard Head')
               
    # Plot Sigmoid-stabilized Snake
    ax.plot(sig_positions[:, 0], sig_positions[:, 1], sig_positions[:, 2], 
            '^-', color='#17becf', label='Sigmoid-Stabilized Snake', linewidth=3, markersize=6)
    # Highlight Head
    ax.scatter(sig_positions[-1, 0], sig_positions[-1, 1], sig_positions[-1, 2], 
               color='#1f77b4', s=100, label='Sigmoid Head')
               
    ax.set_title('3D Snake Robot Configuration (D-H Kinematics)', fontsize=14, fontweight='bold')
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.set_zlabel('Z Position (m)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True)
    
    # Adjust aspect ratio for 3D visualization
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)
    plot_radius = 0.5 * max([x_range, y_range, z_range])
    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    
    plt.tight_layout()
    config_path = 'snake_3d_shapes.png'
    plt.savefig(config_path, dpi=300)
    print(f"Saved 3D configurations plot to: {os.path.abspath(config_path)}")
    plt.close()
    
    # 3. Alternate link scale kinematics validation
    theta_test = np.linspace(-np.pi/4, np.pi/4, 100)
    phi_test = calculate_alternate_link_kinematics(theta_test)
    
    plt.figure(figsize=(8, 5))
    plt.plot(np.degrees(theta_test), np.degrees(phi_test), '-', color='#2ca02c', linewidth=2.5)
    plt.title('Alternate Scale Kinematics: $\\varphi$ vs. $\\theta$', fontsize=14, fontweight='bold')
    plt.xlabel('Actuated Joint Angle $\\theta$ (Degrees)', fontsize=12)
    plt.ylabel('Link Orientation Angle $\\varphi$ (Degrees)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    scale_path = 'alternate_link_kinematics.png'
    plt.savefig(scale_path, dpi=300)
    print(f"Saved alternate link kinematics plot to: {os.path.abspath(scale_path)}")
    plt.close()
    
    print("Kinematics and gait test script successfully prepared.\n")

if __name__ == '__main__':
    test_gait_and_kinematics()
